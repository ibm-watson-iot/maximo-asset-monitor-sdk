from mam.sdk import (entitytype,
                     constants)
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

"""-------------------------------ENTITY TYPE DEMO------------------------
Usage:
1. Create Entity Type - using a json payload
2. Update Entity Type - using a json payload
3. Get Entity Type
4. Remove Entity Type
------------------------------------------------------------------------"""
entitytype_tests_completed = {'create_entity': False, 'remove_entity': False}
# 1. Sample Usage Module: Create Entity Type
with open(entitytype_data_path, 'r') as f:
    try:
        rc_create = entitytype.create_custom_entitytype(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nCreate Entity Type test completed successfully')
        entitytype_tests_completed['create_entity'] = True
    except Exception:
        print(f'FAILED STEP\nFailed create entity type test')

# 2. Sample Usage Module: Delete Entity Type
with open(entitytype_data_path, 'r') as f:
    data = json.load(f)
    try:
        rc_delete = entitytype.remove_entitytype(data['entity_type_name'], credentials=credentials)
        print(f'rc is {rc_delete}. \nDelete Entity Type test completed successfully')
        entitytype_tests_completed['remove_entity'] = True
    except Exception:
        print(f'FAILED STEP\nFailed delete entity type test')

"""-------------------------------CONSTANTS DEMO------------------------
Usage:
1. Create Constants - using a json payload
2. Update Constants - using a json payload
3. Get Constants
4. Remove Constants
----------------------------------------------------------------------"""
constants_tests_completed = {'create_constants': False, 'update_constants': False, 'get_constants': False,
                             'remove_constants': False}
# 1. Sample Usage Module: Create Constants
with open(constants_data_path, 'r') as f:
    try:
        rc_create = constants.create_constants(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nCreate Constants test completed successfully')
        constants_tests_completed['create_constants'] = True
    except Exception as msg:
        print(f'{msg}\nFAILED STEP\nFailed create constants test')

# 2. Sample Usage Module: Update Constants
with open(constants_data_path, 'r') as f:
    data = json.load(f)
    try:
        # update one of the pre-create constants
        update_data = {'constants': [{'name': data['constants'][0]['name'], 'description': 'updated'}]}
        update_data_json = json.dumps(update_data).encode('utf-8')
        print(update_data)
        rc_update = constants.update_constants(update_data_json, credentials=credentials)
        print(f'rc is {rc_delete}. \nUpdate Constants test completed successfully')
        constants_tests_completed['update_constants'] = True
    except Exception as msg:
        print(f'{msg}\nFAILED STEP\nFailed update constants test')

# 3. Sample Usage Module: Get Constants
try:
    get_response = constants.get_constants(credentials=credentials, entity_type_name='shraddha_test_1151_1')
    print(f'constants are {get_response}. \nGet Constants test completed successfully')
    constants_tests_completed['get_constants'] = True
except Exception as msg:
    print(f'{msg}\nFAILED STEP\nFailed get constants test')

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
    constants_tests_completed['remove_constants'] = True
except Exception as msg:
    print(f'{msg}\nFAILED STEP\nFailed delete constants test')


"""-------------------------------SUMMARY OF TESTS------------------------
1. entitytype_tests_completed
2. constants_tests_completed
------------------------------------------------------------------------"""
print('Summary of all tests run')
for name, status in entitytype_tests_completed.items():
    print(f'Test {name} status {status}')
for name, status in constants_tests_completed.items():
    print(f'Test {name} status {status}')