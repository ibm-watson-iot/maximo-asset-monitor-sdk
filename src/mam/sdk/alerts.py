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

query_alerts_schema = {
    "type": "object",
    "properties": {
        "entityTypesFilter": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "dataItem": {"type": "array"},
                }
            }
        },
        "start_ts": {"type": "string"},
        "end_ts": {"type": "string"},
        "groupBy": {
            "type": "array",
            "items": {"type": "string"}
        },
        "time_grain": {"type": "string"}
    }
}


def get_alerts(json_payload, credentials=None):
    """
    get alerts ....
    Uses the following APIs:
        POST /api/asengine/v1/<tenant_id>/queryalertdata

    :param json_payload:
    ```
    {
    "entityTypesFilter": [
        {
            "name": "sample_entity_type_name",
            "dataItem": [
                "alert_data_item_name"
            ]
        }
    ],
    "start_ts": "valid datetime",
    "end_ts": "valid datetime",
    "groupBy": [
        "severity",
        "status",
        "entity_id"
    ],
    "time_grain": "hour"
    }
    ```
    :param credentials: dict analytics-service dev credentials
    :return: json object: list of dict with alert information
    """
    # 1. INPUT CHECKING
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=query_alerts_schema)  # input has valid schema

    # 2. API CONNECTION: GET all constants for a tenant
    logger.debug('Connecting to API')
    body_arguments = json.dumps(payload).encode('utf-8')

    APIClient.environment_info = generate_api_environment(credentials)
    # call api to retrieve alerts
    response = APIClient(api_suffix="asengine",
                         http_method_name="POST",
                         endpoint_suffix="/{orgId}/queryalertdata",
                         body=body_arguments,
                         ).call_api()
    if response.status_code != 200:
        raise Exception('API Client call failed when getting alerts')

    return response.json()


def set_alert():
    """
    do it one at a time?
    :return:
    """
    raise NotImplementedError("In future release")

# Get and set Alerts severity, state, action url
# use post query data for get - will need a json payload
# use api functions for set - the high value or low value etc
