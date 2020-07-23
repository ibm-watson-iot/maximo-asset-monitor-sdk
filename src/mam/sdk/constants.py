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
from iotfunctions.db import (Database)

# mam-sdk modules
from .utils import *
from .parseinput import *
from .apiclient import (APIClient)

from iotfunctions.enginelog import EngineLogging
EngineLogging.configure_console_logging(logging.DEBUG)
logger = logging.getLogger(__name__)

# /constants/v1/{tenantName} POST GET PUT DELETE

# schema expected for creating constants
create_constant_schema = {
    "type": "object",
    "properties": {
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
        }
    },
    "required": ["constants"]
}


def _ui_constant_to_payload(constants, entity_type_name=None):
    """
    convert a list of UI controls to json payload

    :param constants: list of UI control objects/single UI control object
    :return: payload: dict
    """
    if not isinstance(constants, list):
        constants = [constants]
    payload = []
    for c in constants:
        meta = c.to_metadata()
        name = meta['name']
        default = meta.get('value', None)
        del meta['name']
        try:
            del meta['value']
        except KeyError:
            pass
        payload.append({'name': name, 'entityType': entity_type_name, 'enabled': True, 'value': default, 'metadata': meta})

    return payload


def _constant_name_to_payload(constant_names):
    """
    convert a list of constant names
    :param constant_names: str/list of constant names
    :return: dict
    """
    if not isinstance(constant_names, list):
        constant_names = [constant_names]
    payload = []

    for f in constant_names:
        payload.append({'name': f, 'entityType': None})

    return payload


def create_constants(json_payload, credentials=None):
    """
   Register one or more server properties that can be used as entity type
   properties in the AS UI
   Uses the following APIs:
        POST /api/constants/v1/{orgId}

    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    ```
    {
        "entity_type_name":"sample_entity_type_name"
        "constants = [
        {
            "name": "sample_constant_name",
            "datatype" : "number",
            "value": 0.3,
            "default": 0.3,
            "description": "optional"
            # accepted datatypes: 'str'/'string, 'int'/'integer', 'number'/'float','datetime', 'bool'/'boolean'
        }
        ]
    }
    ```
    :return:
    """
    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_constant_schema)  # input has valid schema

    # 2. INPUT PARSING
    entity_type_name = None
    if 'entity_type_name' in payload:
        entity_type_name = payload['entity_type_name']

    constants = None
    if 'constants' in payload:
        constants = payload['constants']
        constants = parse_input_constants(constants)

    create_arguments = json.dumps(_ui_constant_to_payload(constants, entity_type_name)).encode('utf-8')

    # 3. API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to create constants for a tenant
    response = APIClient(api_suffix="constants",
                         http_method_name="POST",
                         endpoint_suffix="/{orgId}",
                         body=create_arguments,
                         ).call_api()

    if response.status_code != 200:
        raise Exception('API Client call failed when adding constants')


def get_constants(entity_type_name=None, credentials=None, ):
    """
    get all constants for a tenant
    Uses the following APIs:
        GET /api/constants/v1/{orgId}

    :param credentials: dict analytics-service dev credentials
    :param entity_type_name: str (optional) filter by entity_type_name
    :return: json object: list of dict with constants information
    """
    # 1. API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')
    query_arguments = {}
    if entity_type_name is not None:
        query_arguments['entityType'] = entity_type_name
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="constants",
                         http_method_name="GET",
                         endpoint_suffix="/{orgId}",
                         query_arguments=query_arguments,
                         ).call_api()
    if response.status_code != 200:
        raise Exception('API Client call failed when getting constants')

    return response.json()


def update_constants(json_payload, credentials=None):
    """
    update constants
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    ```
    {
        "entity_type_name": "optional"
        "constants" = [
        {
            "name": "sample_constant_name",
            "datatype" : "number",
            "default": 0.3,
            "description": "optional"
            # accepted datatypes: 'str'/'string, 'int'/'integer', 'number'/'float','datetime', 'bool'/'boolean'
        }
        ]
    }
    ```
    :return:
    """
    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_constant_schema)  # input has valid schema

    # 2. INPUT PARSING
    entity_type_name = None
    if 'entity_type_name' in payload:
        entity_type_name = payload['entity_type_name']

    constants = None
    if 'constants' in payload:
        constants = payload['constants']
        constants = parse_input_constants(constants)

    update_arguments = json.dumps(_ui_constant_to_payload(constants, entity_type_name)).encode('utf-8')

    # 3. API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="constants",
                         http_method_name="PUT",
                         endpoint_suffix="/{orgId}",
                         body=update_arguments,
                         ).call_api()

    if response.status_code != 200:
        raise Exception('API Client call failed when updating constants')

    return 1


def remove_constants(constant_names, credentials=None):
    """
     Unregister constants by name
     Uses the following APIs:
        DELETE /api/constants/v1/{orgId}

    :param credentials: dict analytics-service dev credentials
    :param constant_names: a str with a constant name or list of constant names
    :return:
    """
    # 1. API CONNECTION
    # :description: to access Watson IOT Platform Analytics.
    logger.debug('Connecting to API')
    body_arguments = json.dumps(_constant_name_to_payload(constant_names)).encode('utf-8')
    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve all constants for a tenant
    response = APIClient(api_suffix="constants",
                         http_method_name="DELETE",
                         endpoint_suffix="/{orgId}",
                         body=body_arguments,
                         ).call_api()
    if response.status_code != 200:
        raise Exception('API Client call failed when deleting constants')
