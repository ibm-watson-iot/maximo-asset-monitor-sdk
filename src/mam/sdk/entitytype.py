# python libraries
import json
from jsonschema import validate
import logging
import importlib
# iotfunctions modules
from iotfunctions.metadata import (BaseCustomEntityType)
from iotfunctions.db import (Database)
# mam-sdk modules
from .utils import *
from .apiclient import (APIClient)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# schema expected for creating entity type
create_schema = {
    "type": "object",
    "properties": {
        "entity_type_name": {"type": "string"},
        "metrics": {"type": "array", "items": {"type": "string"}},
        "constants": {"type": "array", "items": {"type": "string"}},
        "dimensions": {"type": "array", "items": {"type": "string"}},
        "functions": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["entity_type_name"]
}


def _parse_input_functions(functions, environment=None):
    '''
        generate function object from function names

        :param functions list of dicts . example:
        ```
        [{
            'name': 'RandomUniform', #a valid catalog function name
            # PARAMETERS REQUIRED FOR THE FUNCTION
            # For example bif.RandomUniform needs these addition parameters
            'parameters' :
            {
                'min_value' : 0.1,
                'max_value' : 0.2,
                'output_item' : 'discharge_perc'
            }
        }]
        ```
        :param environment json
        :return: a list of functions objects/modules
    '''
    ret_functions = []

    valid_functions = _get_catalog_functions()
    name_to_module = {}
    for item in valid_functions:
        name_to_module[item['name']] = item['moduleAndTargetName']

    # function object from function name
    for f in functions:
        if f['name'] in name_to_module.keys():

            function_path = name_to_module[f['name']].split(".")
            module_path = ".".join(function_path[:-1])
            function_name = function_path[-1]

            try:
                imported_module = importlib.import_module(module_path)
                imported_function = getattr(imported_module, function_name)

                ret_functions.append(imported_function(**f['parameters']))

            except Exception as error:
                print('Could not find target module\n": ' + repr(error))
        else:
            logger.debug(f'{f.name} is not a valid catalog function')

    return ret_functions


def _get_catalog_functions(environment=None):
    '''
        find and returns a list of all catalog functions

        Uses the following APIs:
        PUT    /meta/v1/{orgId}/entityType/{entityTypeName}/archive

        :param environment json
        :return: list of dicts containing all catalog functions
    '''

    # 1. LOADING EXISTING API CREDENTIALS
    '''
        # Getting and Saving API credentials
        # Explore > Usage > Watson IOT Platform Services > Copy to api key
        # Paste contents in environment.json file
        # Explore > Usage > Watson IOT Platform Services > Copy to api token
        ## Paste contents in environment.json file
        # Save file in maximo-asset-monitor-sdk/dev_resources folder
    '''
    logger.debug('Reading API Credentials')
    # TODO: pass as function argument environment
    environment_path = './dev_resources/environment.json'
    with open(environment_path, 'r') as F:
        environment = json.load(F)

    # 2. API CONNECTION: GET ALL CATALOG FUNCTIONS
    logger.debug('Connecting to API')
    APIClient.environment_info = environment
    response = APIClient(api_suffix="catalog",
                         http_method_name="GET",
                         endpoint_suffix="/{orgId}/function",
                         ).call_api()

    return response.json()


def create_custom(json_payload, environment=None, credentials=None):
    '''
    creates an entity type using the given json payload
    expected json schema is as follows:
    ```
        example_schema = {
            "type": "object",
            "properties": {
                "entity_type_name": {"type": "string"},
                "metrics": {"type": "array", "items": {"type": "string"}},
                "constants": {"type": "array", "items": {"type": "string"}},
                "dimensions": {"type": "array", "items": {"type": "string"}},
                "functions": {"type": "array", "items": {"type": "object"}},
            },
            "required": ["entity_type_name"]
        }
    ```
    example example_schema.metrics property
    ```
    [{
        'name': 'metric_a',
        'type': 'str'
        # allowed column types number, boolean, literal/string, timestamp
    }]
    ```
    example example_schema.functions property
    ```
    [{
        'name': 'RandomUniform', #a valid catalog function name
        # PARAMETERS REQUIRED FOR THE FUNCTION
        # For example bif.RandomUniform needs these addition parameters
        'parameters' :
        {
            'min_value' : 0.1,
            'max_value' : 0.2,
            'output_item' : 'discharge_perc'
        }
    }]
    ```
    Uses the following APIs:
    POST /meta/v1/{orgId}/entityType

    :param JSON payload describes metadata required for creating desired entity type
    :return:
    '''

    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_schema)  # input has valid schema

    # 2. INPUT PARSING
    metrics = None
    constants = None
    dimensions = None
    functions = None
    if 'metrics' in payload:
        metrics = payload['metrics']
    if 'constants' in payload:
        constants = payload['constants']
    if 'dimensions' in payload:
        dimensions = payload['dimensions']
    if 'functions' in payload:
        functions = payload['functions']
        functions = _parse_input_functions(functions, environment=environment)

    # 3. LOADING CREDENTIALS
    '''
        # Getting and saving Db credentials
        # Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
        # Paste contents in credentials.json file
        # Save file in maximo-asset-monitor-sdk/dev_resources folder
    '''
    logger.debug('Reading Db Credentials')
    # TODO: pass as function argument
    credentials_path = './dev_resources/credentials.json'
    with open(credentials_path, 'r') as F:
        credentials = json.load(F)

    # 4. DATABASE CONNECTION
    # :description: to access Watson IOT Platform Analytics DB.
    logger.debug('Connecting to Database')
    db = Database(credentials=credentials)
    db_schema = None
    # db_schema = 'bluadmin' #  set if you are not using the default

    # 5. CREATE CUSTOM ENTITY FROM JSON
    # 5.a Instantiate a custom entity type
    entity_type = BaseCustomEntityType(name=payload['entity_type_name'],
                                       db=db,
                                       db_schema=db_schema,
                                       columns=metrics,
                                       constants=constants,
                                       #dimension_columns=dimensions,
                                       functions=functions)
    # 5.b Register entity_type so that it creates a table for input data and appears in the UI
    entity_type.register()

    # CLOSE DB CONNECTION
    db.release_resource()

    return 1


def delete(entity_type_name, environment=None):
    '''
    will first archive and then delete entity type

    Uses the following APIs:
    PUT    /meta/v1/{orgId}/entityType/{entityTypeName}/archive
    DELETE /meta/v1/{orgId}/entityType/{entityTypeName}

    :param entity_type_name str name of entity type to delete
    :return:
    '''
    # 1. LOADING EXISTING API CREDENTIALS
    '''
        # Getting and Saving API credentials
        # Explore > Usage > Watson IOT Platform Services > Copy to api key
        # Paste contents in environment.json file
        # Explore > Usage > Watson IOT Platform Services > Copy to api token
        ## Paste contents in environment.json file
        # Save file in maximo-asset-monitor-sdk/dev_resources folder
    '''
    logger.debug('Reading API Credentials')
    # TODO: pass as function argument
    environment_path = './dev_resources/environment.json'
    with open(environment_path, 'r') as F:
        environment = json.load(F)

    # 2. API CONNECTION: ARCHIVE DELETE ENTITY TYPE
    logger.debug('Connecting to API')
    path_arguments = {
        'entityTypeName': entity_type_name
    }
    APIClient.environment_info = environment
    # 2.a Archive entity type (required before deleting)
    response = APIClient(api_suffix="meta",
                         http_method_name="PUT",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/archive",
                         path_arguments=path_arguments
                         ).call_api()

    if response.status_code == 200:
        # 2.b Delete archived entity type
        APIClient(api_suffix="meta",
                  http_method_name="DELETE",
                  endpoint_suffix="/{orgId}/entityType/{entityTypeName}",
                  path_arguments=path_arguments
                  ).call_api()
    else:
        logger.debug(f'Unable to archive entity type. Entity type name : {entity_type_name}')

    return 1
