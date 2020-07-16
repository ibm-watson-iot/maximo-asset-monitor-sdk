# python libraries
import json
import logging
import importlib
from jsonschema import validate
from sqlalchemy import Column

# iotfunctions modules
from iotfunctions.metadata import (BaseCustomEntityType)
from iotfunctions.db import (Database)
from iotfunctions import ui

# mam-sdk modules
from .utils import *
from .apiclient import (APIClient)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _parse_input_columns(columns):
    """
    generate sqlalchemy Column from user defined columns

    :param columns: list of dicts . example:
    ```
    [{
        'name': 'sample_column_name',
        'datatype' : 'str',
        # accepted types: 'str'/'string, 'int'/'integer', 'float','datetime', 'bool'/'boolean'
    }]
    ```
    :return: a list of sqlalchemy Columns
    """
    ret_columns = []

    name_to_type = {}
    for c in columns:
        name_to_type[c['name']] = c['datatype']

    for name, type in name_to_type.items():
        ret_columns.append(Column(name.lower(), sqlalchemy_type(type)))

    return ret_columns


def _parse_input_constants(constants):
    """
    generate sqlalchemy Column from user defined columns (for UISingle constants only)
    TODO: add support for UIMulti. Currently, it's not documented how to

    :param constants: list of dicts; example:
    ```
    [{
        'name': 'sample_constant_name',
        'datatype' : 'str',
        'default': 0.3,
        'description': 'optional'
        # accepted datatypes: 'str'/'string, 'int'/'integer', 'float','datetime', 'bool'/'boolean'
    }]
    ```
    :return: ui_control constants accepted BasicCustomEntity
    """
    ret_constants = []

    for c in constants:
        if c['datatype'] == 'datetime':
            c['default'] = validate_and_normalize_timestamp(c['default'])

        ret_constants.append(
            ui.UISingle(name=c['name'],
                        description=c['description'],
                        datatype=python_type(c['datatype']),
                        default=c['default']
                        )
        )

    return ret_constants


def _parse_input_functions(functions, credentials=None):
    """
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
    :param credentials: dicts analytics-service devcredentials
    :return: a list of functions objects/modules
    """
    ret_functions = []

    valid_functions = _get_catalog_functions(credentials=credentials)
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


def _get_catalog_functions(credentials=None):
    """
    find and returns a list of all catalog functions

    Uses the following APIs:
    PUT    /meta/v1/{orgId}/entityType/{entityTypeName}/archive

    :param credentials: dict analytics-service dev credentials
    :return: list of dicts containing all catalog functions
    """

    # API CONNECTION: GET ALL CATALOG FUNCTIONS
    logger.debug('Connecting to API')
    APIClient.environment_info = generate_api_environment(credentials)
    response = APIClient(api_suffix="catalog",
                         http_method_name="GET",
                         endpoint_suffix="/{orgId}/function",
                         ).call_api()

    return response.json()


def create_custom(json_payload, credentials=None, **kwargs):
    """
    creates an entity type using the given json payload
    Uses the following APIs:
    POST /meta/v1/{orgId}/entityType

    :param json_payload: JSON describes metadata required for creating desired entity type
    expected json schema is as follows:
    ```
        example_schema = {
            "type": "object",
            "properties": {
                "entity_type_name": {"type": "string"},
                "metrics": {"type": "array", "items": {"type": "object"}},
                "constants": {"type": "array", "items": {"type": "object"}},
                "dimensions": {"type": "array", "items": {"type": "object"}},
                "functions": {"type": "array", "items": {"type": "object"}},
            },
            "required": ["entity_type_name"]
        }
    ```
    example example_schema.metrics/dimensions property
    ```
    [{
        'name': 'metric_a',
        'type': 'str'
        # allowed column types number, boolean, literal/string, timestamp
    }]
    ```
    example example_schema.constants property
    ```
    [{
        'name': 'sample_constant_name',
        'datatype' : 'str',
        'default': 0.3,
        'description': 'optional'
        # accepted types: 'str'/'string, 'int'/'integer', 'float','datetime', 'bool'/'boolean'
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
    :param credentials: dict analytics-service dev credentials
    :param **kwargs {
        drop_existing bool delete existing table and rebuild the entity type table in Db
        db_schema str if no schema is provided will use the default schema
    }

    :return:
    """

    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_custom_schema)  # input has valid schema

    # 2. INPUT PARSING
    metrics = None
    constants = None
    dimensions = None
    functions = None
    if 'metrics' in payload:
        metrics = payload['metrics']
        metrics = _parse_input_columns(metrics)
    if 'constants' in payload:
        constants = payload['constants']
        constants = _parse_input_constants(constants)
    if 'dimensions' in payload:
        dimensions = payload['dimensions']
        dimensions = _parse_input_columns(dimensions)
    if 'functions' in payload:
        functions = payload['functions']
        functions = _parse_input_functions(functions, credentials=credentials)

    # 3. DATABASE CONNECTION
    # :description: to access Watson IOT Platform Analytics DB.
    logger.debug('Connecting to Database')
    db = Database(credentials=credentials)

    # 4. CREATE CUSTOM ENTITY FROM JSON
    # 4.a Instantiate a custom entity type
    # required columns: _timestamp:evt_timestamp  _entity_id:deviceid
    entity_type = BaseCustomEntityType(name=payload['entity_type_name'],
                                       db=db,
                                       columns=metrics,
                                       constants=constants,
                                       dimension_columns=dimensions,
                                       functions=functions,
                                       **kwargs)
    # 4.b Register entity_type so that it creates a table for input data and appears in the UI
    # Publish kpi to register kpis and constants to appear in the UI
    entity_type.register(publish_kpis=True)

    # 5. CLOSE DB CONNECTION
    db.release_resource()

    return 1


def create_metrics(json_payload, credentials=None):
    """
    add metrics to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    return 1


def update_metrics(json_payload, credentials=None):
    """

    :param json_payload:
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    return 1


def remove_metrics(json_payload, credentials=None):
    """

    :param json_payload:
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    return 1


def create_functions(json_payload, credentials=None):
    """
    add kpi functions to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    return 1


def update_functions(json_payload,  credentials=None):
    """
    add kpi functions to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    return 1


def remove_functions(json_payload, credentials=None):
    """

    :param json_payload:
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    return 1


def create_constants(json_payload, credentials=None):
    """
    add constants to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    return 1


def update_constants(json_payload, credentials=None):
    """
    add constants to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    return 1


def remove_constants(json_payload, credentials=None):
    """
    add constants to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    return 1


def delete(entity_type_name, credentials=None):
    """
    will first archive and then delete entity type

    Uses the following APIs:
    PUT    /meta/v1/{orgId}/entityType/{entityTypeName}/archive
    DELETE /meta/v1/{orgId}/entityType/{entityTypeName}

    :param credentials: dict analytics-service dev credentials
    :param entity_type_name: str name of entity type to delete
    :return:
    """

    # 1. API CONNECTION: ARCHIVE DELETE ENTITY TYPE
    logger.debug('Connecting to API')
    path_arguments = {
        'entityTypeName': entity_type_name
    }
    APIClient.environment_info = generate_api_environment(credentials)
    # 1.a Archive entity type (required before deleting)
    response = APIClient(api_suffix="meta",
                         http_method_name="PUT",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/archive",
                         path_arguments=path_arguments
                         ).call_api()

    if response.status_code == 200:
        # 1.b Delete archived entity type
        APIClient(api_suffix="meta",
                  http_method_name="DELETE",
                  endpoint_suffix="/{orgId}/entityType/{entityTypeName}",
                  path_arguments=path_arguments
                  ).call_api()
    else:
        logger.debug(f'Unable to archive entity type. Entity type name : {entity_type_name}')

    return 1
