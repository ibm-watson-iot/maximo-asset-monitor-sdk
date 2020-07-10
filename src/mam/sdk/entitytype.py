import json
from jsonschema import validate
from .utils import *

# schema expected from creating entity type
create_schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "status": {"type": "boolean"},
        "value_a": {"type": "number"},
        "value_b": {"type": "number"},
    },
}


def create(json_payload):
    '''
    description

    Args:
        JSON payload

    Returns:
    '''

    # INPUT CHECKING
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_schema)  # input has valid schema

    return 1
