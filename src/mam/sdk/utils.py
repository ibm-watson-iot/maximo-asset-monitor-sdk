import json
import re
import logging
from string import punctuation, whitespace
from sqlalchemy import Integer, String, Float, DateTime, Boolean, SmallInteger
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

delimiter_pattern = "|".join([re.escape(delimiter) for delimiter in punctuation + whitespace + "t" + "T"])
compiled_delimiter_pattern = re.compile(delimiter_pattern)


def validateJSON(json_payload):
    """validate that the input parameter is a valid json file"""
    try:
        payload = json.loads(json_payload)
    except ValueError as err:
        return False
    return payload


def convert_to_datetime(timestamp_string):
    """convert string input to datetime.datetime type"""
    if timestamp_string is None:
        return None

    split_timestamp_string = compiled_delimiter_pattern.split(timestamp_string)

    timestamp_values = [int(value) for value in split_timestamp_string]
    return datetime(*timestamp_values)


def validate_and_normalize_timestamp(timestamp_string):
    """convert string input to datetime.datetime type"""
    if timestamp_string is None:
        return None

    datetime_timestamp = convert_to_datetime(timestamp_string)
    return datetime_timestamp.isoformat(sep=" ")


# converting user input 'type' to sqlalchemy type
_type_sql_dict = {
    'int': Integer,
    'integer': Integer,
    'string': String,
    'str': String,
    'float': Float,
    'datetime': DateTime,
    'bool': Boolean,
    'boolean': Boolean
}


def sqlalchemy_type(type):
    """Return the closest sql type for a given string"""
    if type in _type_sql_dict:
        return _type_sql_dict[type.lower()]
    else:
        raise NotImplementedError(
            "You may add custom `sqltype` to `" + str(type) + "` assignment in `_type_sql_dict`.")


# converting user input 'type' to sqlalchemy type
_type_python_dict = {
    'int': int,
    'integer': int,
    'string': str,
    'str': str,
    'float': float,
    'datetime': datetime,
    'bool': bool,
    'boolean': bool
}


def python_type(type):
    """Return the closest python type for a given string"""
    if type in _type_python_dict:
        return _type_python_dict[type.lower()]
    else:
        raise NotImplementedError(
            "You may add custom `datatype` to `" + str(type) + "` assignment in `_type_python_dict`.")


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
                "required": ["name", "datatype"]
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
