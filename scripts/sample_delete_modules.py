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
credentials_path = './dev_resources/credentials.json'
entitytype_data_path = './data/sample_usage_data.json'
constants_data_path = './data/sample_constant_data.json'

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

"""-------------------------------FUNCTIONS DEMO------------------------
Usage:
4. (X) Remove Function
------------------------------------------------------------------------"""
tests_completed = {'remove_functions': False}
# 4. Sample Usage Module: Delete Entity Type
with open(entitytype_data_path, 'r') as f:
    data = json.load(f)
    function_created = [c['name'] for c in data['functions']][0]
    entity_type_name = data['entity_type_name']
print(f'Function enqueued for deletion: {function_created}')
try:
    rc_delete = kpifunction.remove_function(entity_type_name, function_created, credentials=credentials)
    print(f'rc is {rc_delete}. \nDelete Function test completed successfully')
    tests_completed['remove_functions'] = True
except Exception as msg:
    print(f'FAILED STEP: {msg}\nFailed delete function test')

"""-------------------------------DIMENSIONS DELETE DEMO------------------------
Usage:
4. (X) Remove Dimension 
------------------------------------------------------------------------------"""
with open(entitytype_data_path, 'r') as f:
    data = json.load(f)
    dimension_created = [d['name'] for d in data['dimensions']]
    entity_type_name = data['entity_type_name']
try:
    dimension.remove_dimensions(credentials=credentials,  dimension_names=dimension_created,
                               entity_type_name=entity_type_name)
    tests_completed['remove_dimensions'] = True
except Exception as msg:
    print(f'FAILED STEP: {msg}\nFailed delete dimension test')

"""-------------------------------CONSTANTS DEMO------------------------
Usage:
4. (X) Remove Constants
----------------------------------------------------------------------"""
tests_completed['remove_constants'] = False
# 4. Sample Usage Module: Remove Constants
# collect all constants created so far
with open(entitytype_data_path, 'r') as f:
    data = json.load(f)
    constants_created = [c['name'] for c in data['constants']]
with open(constants_data_path, 'r') as f:
    data = json.load(f)
    temp_constants_created = [c['name'] for c in data['constants']]
    constants_created.extend(temp_constants_created)
print(f'Constants enqueued for deletion: {constants_created}')
try:
    rc_delete = constants.remove_constants(constants_created, credentials=credentials)
    print(f'rc is {rc_delete}. \nRemove Constants test completed successfully')
    tests_completed['remove_constants'] = True
except Exception as msg:
    print(f'FAILED STEP: {msg}\nFailed delete constants test')


"""-------------------------------ENTITY TYPE DEMO------------------------
Usage:
4. (X) Remove Entity Type
------------------------------------------------------------------------"""
tests_completed['remove_entity'] = False
# 2. Sample Usage Module: Delete Entity Type
with open(entitytype_data_path, 'r') as f:
    data = json.load(f)
    try:
        rc_delete = entitytype.remove_entitytype(data['entity_type_name'], credentials=credentials)
        print(f'rc is {rc_delete}. \nDelete Entity Type test completed successfully')
        tests_completed['remove_entity'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed delete entity type test')


"""-------------------------------SUMMARY OF DELETE TESTS------------------------
------------------------------------------------------------------------------"""
print('Summary of all tests run')
for name, status in tests_completed.items():
    print(f'Test {name} status {status}')