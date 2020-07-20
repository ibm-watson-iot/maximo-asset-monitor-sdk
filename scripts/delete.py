from mam.sdk import (entitytype,
                     constants,
                     kpifunction)
import json

#DEFINE PATH TO REQUIRED FILES
#relative to where you run script from
credentials_path = './dev_resources/credentials.json'
entitytype_data_path = './scripts/sample_usage_data.json'
constants_data_path = './scripts/sample_constant_data.json'

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
tests_completed = {'remove_entity': False}
# 4. Sample Usage Module: Delete Entity Type
with open(entitytype_data_path, 'r') as f:
    data = json.load(f)
    function_created = [c['name'] for c in data['functions']][0]
    entity_type_name = data['entity_type_name']
print(f'Function enqueued for deletion: {function_created}')
try:
    rc_delete = kpifunction.remove_function(entity_type_name, function_created, credentials=credentials)
    print(f'rc is {rc_delete}. \nDelete Entity Type test completed successfully')
    tests_completed['remove_entity'] = True
except Exception as msg:
    print(f'FAILED STEP: {msg}\nFailed delete entity type test')

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
tests_completed = {'remove_entity': False}
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
1. function tests
2. constants tests
3. entitytype tests
------------------------------------------------------------------------------"""
print('Summary of all tests run')
for name, status in tests_completed.items():
    print(f'Test {name} status {status}')