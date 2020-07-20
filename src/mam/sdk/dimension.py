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


def add_dimensions(json_payload, credentials=None):
    """
    add metrics to a given entity type
    :param credentials: dict analytics-service dev credentials
    :param json_payload:
    :return:
    """
    raise Exception("Not supported in the sdk")


def update_dimensions(json_payload, credentials=None):
    """

    :param json_payload:
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    raise Exception("Not supported in the sdk")


def get_dimensions(entity_type_name, crednetials=None):
    """

    :param entity_type_name:
    :param crednetials:
    :return:
    """
    raise Exception("Not supported in the sdk")


def remove_dimensions(json_payload, credentials=None):
    """

    :param json_payload:
    :param credentials: dict analytics-service dev credentials
    :return:
    """
    raise Exception("Not supported in the sdk")