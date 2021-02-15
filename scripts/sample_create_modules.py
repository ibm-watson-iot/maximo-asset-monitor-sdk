#  | * IBM Confidential
#  | * OCO Source Materials
#  | * 5737-M66
#  | * © Copyright IBM Corp. 2020
#  | * The source code for this program is not published or otherwise divested of its
#  | * trade secrets, irrespective of what has been deposited with the U.S.
#  | * Copyright Office.

from mam.sdk import (entitytype,
                     constants,
                     kpifunction,
                     dimension)
import json

#DEFINE PATH TO REQUIRED FILES
#relative to where you run script from
credentials_path = '../dev_resources/credentials.json'
entitytype_data_path = '../data/sample_usage_data.json'
constants_data_path = '../data/sample_constant_data.json'
function_data_path = '../data/sample_function_data.json'
dimension_data_path = '../data/sample_dimension_data.json'

#LOADING DATABASE CREDENTIALS
'''
# Getting and saving Db credentials
# Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
# Paste contents in credentials.json file
# Save file in maximo-asset-monitor-sdk/dev_resources folder (one example)
'''
print('Reading Analytics Credentials')
with open(credentials_path, 'r') as F:
    credentials = json.load(F)

tests_completed = {}
"""-------------------------------ENTITY TYPE DEMO------------------------
Usage:
1. (X) Create Entity Type - using a json payload
------------------------------------------------------------------------"""
tests_completed['create_entity'] = False
# 1. Sample Usage Module: Create Entity Type
with open(entitytype_data_path, 'r') as f:
    try:
        rc_create = entitytype.create_custom_entitytype(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nCreate Entity Type test completed successfully')
        tests_completed['create_entity'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed create entity type test')


"""-------------------------------ADD FUNCTION TO ENTITY TYPE DEMO------------------------
Usage:
1. (X) Add Function - using a json payload
------------------------------------------------------------------------------------------"""
tests_completed['add_functions'] = False
# 1. Sample Usage Module: Create Entity Type
with open(function_data_path, 'r') as f:
    try:
        rc_create = kpifunction.add_functions(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nAdd KPI Functions test completed successfully')
        tests_completed['add_functions'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed add functions test')

"""-------------------------------ADD DIMENSION DATA TO ENTITY TYPE DEMO--------------------
Usage:
1. (X) Add Dimension - using a json payload
------------------------------------------------------------------------------------------"""
tests_completed['add_dimension_data'] = False
# 1. Sample Usage Module: Create Entity Type
with open(dimension_data_path, 'r') as f:
    try:
        rc_create = dimension.add_dimensions_data(f.read(), credentials=credentials, )
        print(f'rc is {rc_create}. \nAdd dimension data test completed successfully')
        tests_completed['add_dimension_data'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed add dimension data test')


"""-------------------------------CONSTANTS DEMO------------------------
Usage:
1. (X) Create Constants - using a json payload
----------------------------------------------------------------------"""
tests_completed['create_constants'] = False
# 1. Sample Usage Module: Create Constants
with open(constants_data_path, 'r') as f:
    try:
        rc_create = constants.create_constants(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nCreate Constants test completed successfully')
        tests_completed['create_constants'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed create constants test')


"""-------------------------------SUMMARY OF CREATION TESTS------------------------
---------------------------------------------------------------------------------"""
print('Summary of all tests run')
for name, status in tests_completed.items():
    print(f'Test {name} status {status}')