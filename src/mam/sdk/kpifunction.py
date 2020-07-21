#  © Copyright IBM Corp. 2020

# python libraries
import json
import logging
from jsonschema import validate

# iotfunctions modules
from iotfunctions.metadata import (BaseCustomEntityType)
from iotfunctions.db import (Database)

# mam-sdk modules
from .utils import *
from .parseinput import *
from .apiclient import (APIClient)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# schema expected for creating kpi functions for entity type
create_kpifunction_schema = {
    "type": "object",
    "properties": {
        "functions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "parameters": {"type": "object"},
                },
                "required": ["name"]
            }
        },
        "entity_type_name": {"type": "string"}
    },
    "required": ["functions"]
}


def add_functions(json_payload, credentials=None):
    """
    add kpi functions to a given entity type
    Uses the following APIs:
        POST  /api/kpi/v1/{orgId}/entityType/{entityTypeName}/kpiFunction

    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    ```
    {
        "entity_type_name": "sample_entity_type_name"
        "functions": [
        {
            "name": "RandomUniform", #a valid catalog function name
            # PARAMETERS REQUIRED FOR THE FUNCTION
            # For example bif.RandomUniform needs these additional parameters
            "parameters" :
            {
                "min_value" : 0.1,
                "max_value" : 0.2,
                "output_item" : "discharge_perc"
            }
        }
        ]
    }
    ```
    :return:
    """
    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_kpifunction_schema)  # input has valid schema

    # 2. INPUT PARSING
    if 'entity_type_name' not in payload:
        raise Exception('No Entity Type was specified')

    functions = None
    if 'functions' in payload:
        functions = payload['functions']
        functions = parse_input_functions(functions, credentials=credentials)

    # 3. DATABASE CONNECTION
    # :description: to access Watson IOT Platform Analytics DB.
    logger.debug('Connecting to Database')
    db = Database(credentials=credentials)

    # 4. CREATE CUSTOM ENTITY FROM JSON
    # 4.a Instantiate a custom entity type
    entity_type = BaseCustomEntityType(name=payload['entity_type_name'],
                                       db=db,
                                       functions=functions)
    # 4.b Publish kpi to register kpis and constants to appear in the UI
    entity_type.publish_kpis()

    # 5. CLOSE DB CONNECTION
    db.release_resource()

    return 1


def get_functions(entity_type_name, credentials=None):
    """
        get all kpi functions for an entity type
        Uses the following APIs:
            GET /kpi/v1/{orgId}/entityType/{entityTypeName}/kpiFunction

        :param entity_type_name: str name of entity type
        :param credentials: dict analytics-service dev credentials
        :return: json object: list of dict with kpi functions
        """
    # 1. API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')
    path_arguments = {}
    if entity_type_name is not None:
        path_arguments['entityTypeName'] = entity_type_name
    else:
        raise Exception("No Entity Type Name provided")

    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="kpi",
                         http_method_name="GET",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/kpiFunction",
                         path_arguments=path_arguments,
                         ).call_api()
    return response.json()


# TODO: Implement this function
def update_functions(json_payload, credentials=None):
    """
    update kpi functions for a given entity type.
    Uses the following APIs:
    PUT /kpi/v1/{orgId}/entityType/{entityTypeName}/kpiFunction/{kpiFunctionName}

    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    # do the add but get the 'name' first -> is user defined
    # then
    raise Exception("Not supported in the sdk. Configure through UI")


def remove_function(entity_type_name, kpi_name, credentials=None):
    """
    delete a single kpi functions from an entity type's functions
        Uses the following APIs:
            DELETE /kpi/v1/{orgId}/entityType/{entityTypeName}/kpiFunction/{kpiFunctionName}

    :param entity_type_name: str name of entity type to which function belongs
    :param kpi_name: str name of kpi function to be deleted. example kpi_name
    'b90602b0-6f7f-4f6d-9f98-25a33becb313'.
    Note: this is not the same as the function_name like: 'Random Uniform'
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    if kpi_name is None:
        raise Exception(f'No kpi functions {kpi_name} found for entity type {entity_type_name}')

    # 2. API CONNECTION
    # :description: to access Watson IOT Platform Analytics.
    logger.debug('Connecting to API')
    APIClient.environment_info = generate_api_environment(credentials)
    path_arguments = {'entityTypeName': entity_type_name, 'kpiFunctionName': kpi_name}
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="kpi",
                         http_method_name="DELETE",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/kpiFunction/{kpiFunctionName}",
                         path_arguments=path_arguments,
                         ).call_api()
    try:
        msg = 'Function deletion status: %s' % (response.data.decode('utf-8'))
    except AttributeError:
        msg = 'Function deletion status: %s' % response
    logger.info(msg)
    return 1
