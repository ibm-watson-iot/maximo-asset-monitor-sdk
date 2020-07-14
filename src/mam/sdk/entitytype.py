import json
from jsonschema import validate

from iotfunctions.metadata import EntityType, BaseCustomEntityType
from iotfunctions.db import Database

import logging
from iotfunctions.enginelog import EngineLogging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    /meta/v1/{orgId}/entityType

    Args:
        JSON payload

    Returns:
    '''

    # INPUT CHECKING
    print('HERE')
    logger.debug('Performing Input Checking')
    payload = validateJSON(json_payload)  # input is valid json
    validate(instance=payload, schema=create_schema)  # input has valid schema

    # LOADING EXISTING CREDENTIALS
    '''
        # Getting Db credentials
        # Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
        # Paste contents in credentials.json file
        # Save file in maximo-asset-monitor-sdk/dev_resources folder
    '''
    logger.debug('Reading Credentials')
    credentials_path = './dev_resources/credentials.json'
    with open(credentials_path) as F:
        credentials = json.loads(F.read())

    # DATABASE CONNECTION
    # to access Watson IOT Platform Analytics DB.
    logger.debug('Connection to Database')
    db = Database(credentials=credentials)
    db_schema = None
    # db_schema = 'bluadmin' #  set if you are not using the default

    # CLOSE DB CONNECTION
    db.release_resource()

    return 1


'''
class BaseCustomEntityType(EntityType):
 Base class for custom entity types

 timestamp = 'evt_timestamp'

 def __init__(self, name, db, columns=None, constants=None, granularities=None, functions=None,
              dimension_columns=None, generate_days=0, generate_entities=None, drop_existing=False, db_schema=None,
              description=None, output_items_extended_metadata=None, **kwargs)

 auto_create_table = True keyword arg
'''
