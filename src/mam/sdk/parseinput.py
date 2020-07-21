#  © Copyright IBM Corp. 2020

# python libraries
import importlib
from sqlalchemy import Column

# iotfunctions modules
from iotfunctions import ui

# mam-sdk modules
from .utils import *
from .apiclient import (APIClient)


def parse_input_columns(columns):
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


def parse_input_constants(constants):
    """
    generate sqlalchemy Column from user defined columns (for UISingle constants only)
    TODO: add support for UIMulti. Currently, it's not documented how to

    :param constants: list of dicts; example:
    ```
    [{
        'name': 'sample_constant_name',
        'datatype' : 'number',
        'default': 0.3,
        'description': 'optional'
        # accepted datatypes: 'str'/'string, 'int'/'integer', 'number'/'float','datetime', 'bool'/'boolean'
    }]
    ```
    :return: ui_control constants accepted BasicCustomEntity
    """
    ret_constants = []

    for c in constants:
        datatype, default, description = None, None, None
        if 'datatype' in c:
            datatype = python_type(c['datatype'])
        if 'default' in c:
            default = c['default']
        if 'description' in c:
            description = c['description']

        if datatype is not None and default is not None and c['datatype'] == 'datetime':
            default = validate_and_normalize_timestamp(default)

        ret_constants.append(
            ui.UISingle(name=c['name'],
                        description=description,
                        datatype=datatype,
                        default=default
                        )
        )

    return ret_constants


def parse_input_functions(functions, credentials=None):
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

    valid_functions = get_catalog_functions(credentials=credentials)
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


def get_catalog_functions(credentials=None):
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