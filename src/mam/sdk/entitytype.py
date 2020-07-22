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

# schema expected for creating entity type
create_custom_schema = {
    "type": "object",
    "properties": {
        "entity_type_name": {"type": "string"},
        "metrics": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["name", "datatype"]
            }
        },
        "constants": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "datatype": {"type": "string"},
                    "default": {},
                    "description": {"type": "string"}
                },
                "required": ["name"]
            }
        },
        "dimensions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["name", "datatype"]
            }
        },
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
    },
    "required": ["entity_type_name"]
}


def create_custom_entitytype(json_payload, credentials=None, **kwargs):
    """
    creates an entity type using the given json payload
    Uses the following APIs:
        POST /meta/v1/{orgId}/entityType
        POST /api/kpi/v1/{orgId}/entityType/{entity_type_name}/kpiFunctions/import
        POST /api/constants/v1/{orgId}

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
                "metric_timestamp_column_name":{"type": "string"}
            },
            "required": ["entity_type_name"]
        }
    ```
    example example_schema.metrics/dimensions property
    ```
    [{
        'name': 'metric_a',
        'datatype': 'str'
        # allowed column types number, boolean, literal/string, timestamp
        # accepted datatypes: 'str'/'string, 'int'/'integer', 'number'/'float','datetime', 'bool'/'boolean'
    }]
    ```
    example example_schema.constants property
    ```
    [{
        'name': 'sample_constant_name',
        'datatype' : 'number',
        'value': 0.3,
        'default': 0.3,
        'description': 'optional'
        # accepted datatypes: 'str'/'string, 'int'/'integer', 'number'/'float','datetime', 'bool'/'boolean'
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
        metrics = parse_input_columns(metrics)
    if 'constants' in payload:
        constants = payload['constants']
        constants = parse_input_constants(constants)
    if 'dimensions' in payload:
        dimensions = payload['dimensions']
        dimensions = parse_input_columns(dimensions)
    if 'functions' in payload:
        functions = payload['functions']
        functions = parse_input_functions(functions, credentials=credentials)

    # 3. DATABASE CONNECTION
    # :description: to access Watson IOT Platform Analytics DB.
    logger.debug('Connecting to Database')
    db = Database(credentials=credentials)

    # 4. CREATE CUSTOM ENTITY FROM JSON
    # 4.a Instantiate a custom entity type
    #overrides the _timestamp='evt_timestamp'
    if 'metric_timestamp_column_name':
        BaseCustomEntityType._timestamp = payload['metric_timestamp_column_name']
    # TODO: BaseCustomEntityType.timestamp= add user defined timestamp column
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


def remove_entitytype(entity_type_name, credentials=None):
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
        response = APIClient(api_suffix="meta",
                             http_method_name="DELETE",
                             endpoint_suffix="/{orgId}/entityType/{entityTypeName}",
                             path_arguments=path_arguments
                             ).call_api()
        if response.status_code != 200:
            logger.warning(f'Entity Type {entity_type_name} was not deleted')
    else:
        logger.debug(f'Unable to archive entity type. Entity type name : {entity_type_name}')

    return 1
