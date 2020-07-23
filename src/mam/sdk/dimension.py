#  | * IBM Confidential
#  | * OCO Source Materials
#  | * 5737-M66
#  | * © Copyright IBM Corp. 2020
#  | * The source code for this program is not published or otherwise divested of its
#  | * trade secrets, irrespective of what has been deposited with the U.S.
#  | * Copyright Office.

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

from iotfunctions.enginelog import EngineLogging
EngineLogging.configure_console_logging(logging.DEBUG)
logger = logging.getLogger(__name__)

# schema expected for creating constants
create_dimension_data_schema = {
    "type": "object",
    "properties": {
        "entity_type_name": {"type": "string"},
        "dimension_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "entity_id": {"type": "string"},
                    "value": {},
                    "datatype": {"type": "string"}
                },
                "required": ["name", "entity_id", "value"]
            },
        }
    },
    "required": ["dimension_data", "entity_type_name"]
}


def _dimension_data_to_payload(dimensions):
    """
    convert a list of dimension data objects to json payload

    :param dimensions: list of dimension data objects
    :return: payload: dict
    """
    if not isinstance(dimensions, list):
        dimensions = [dimensions]
    payload = []
    for d in dimensions:
        payload.append(d)

    return payload


def add_dimensions_data(json_payload, credentials=None):
    """
    add dimensional data to a given entity type
    Uses API:
        POST /master/v1/{orgId}/entityType/{entityTypeName}/dimensional

    Note:
    if there is no dimensional value with name specified, this will create a table
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    ```
    {
        "entity_type_name":"sample_entity_type_name"
        "dimension_data":[
            {
                "name": "sample_dimension_name",
                "entity_id" : "sample_entity_name",
                "value": 0.3
                "datatype": "optional"
                # accepted datatypes: 'str'/'string, 'int'/'integer', 'number'/'float','datetime', 'bool'/'boolean'
            }
        ]

    }
    :return:
    """
    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    # validate(instance=payload, schema=create_dimension_data_schema)  # input has valid schema

    # 2. INPUT PARSING
    entity_type_name = payload['entity_type_name']
    dimension_data = payload['dimension_data']

    create_arguments = parse_input_dimension_data(dimension_data)
    create_arguments = json.dumps(_dimension_data_to_payload(create_arguments)).encode('utf-8')

    # API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')

    path_arguments = {'entityTypeName': entity_type_name}
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="master",
                         http_method_name="POST",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/dimensional",
                         path_arguments=path_arguments,
                         body=create_arguments
                         ).call_api()

    if response.status_code != 200:
        raise Exception('API Client call failed when adding dimensions')

    return response.json()


def update_dimensions_data(json_payload, credentials=None):
    """
    same as add_dimesion_data
    if the dimension exists it is updated with new value
    if not a new dimension and value corresponding value is added

    :param json_payload:
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    return add_dimension_data(json_payload, credentials)


def get_dimensions_data(entity_type_name, credentials=None):
    """
    get all the dimensional data for an entity type
    Uses API:
        POST /master/v1/{orgId}/entityType/{entityTypeName}/dimensional
    :param entity_type_name: str name of entity type
    :param credentials: dict analytics-service dev credentials
    :return: json (list of dict) with dimension data information
    """
    # 1. API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')

    path_arguments = {'entityTypeName': entity_type_name}
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="master",
                         http_method_name="GET",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/dimensional",
                         path_arguments=path_arguments
                         ).call_api()
    if response.status_code != 200:
        raise Exception('API Client call failed when getting dimensions')

    return response.json()


def remove_dimensions(dimension_names, entity_type_name, credentials=None):
    """
    Delete dimension data by name
         Uses the following APIs:
            DELETE /master/v1/{orgId}/entityType/{entityTypeName}/dimensional

    :param entity_type_name: sting name of entity type
    :param dimension_names: list of string names of dimensions
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    # 1. API CONNECTION
    # :description: to access Watson IOT Platform Analytics.
    logger.debug('Connecting to API')

    if not isinstance(dimension_names, list):
        dimension_names = [dimension_names]

    query_arguments = {'dimensionNames': dimension_names}
    collection_formats = {'dimensionNames': 'csv'}

    path_arguments = {'entityTypeName': entity_type_name}
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="master",
                         http_method_name="DELETE",
                         endpoint_suffix="/{orgId}/entityType/{entityTypeName}/dimensional",
                         path_arguments=path_arguments,
                         query_arguments=query_arguments,
                         collection_formats=collection_formats
                         ).call_api()

    if response.status_code != 200:
        raise Exception('API Client call failed when deleting dimensions')

    return response.json()
