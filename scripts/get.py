#  © Copyright IBM Corp. 2020

from mam.sdk import (entitytype,
                     constants,
                     kpifunction)
import json

#DEFINE PATH TO REQUIRED FILES
#relative to where you run script from
credentials_path = './dev_resources/credentials.json'

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
3. () Get Entity Type
------------------------------------------------------------------------"""


"""-------------------------------FUNCTIONS (ENTITY TYPE) DEMO------------------------
Usage:
3. (X) Get all functions
-------------------------------------------------------------------------------------"""
tests_completed['get_functions'] = False
# 3. Sample Usage Module: Get Entity Type Functions
try:
    get_response = kpifunction.get_functions(credentials=credentials,  entity_type_name='shraddha_test_1151_1')
    print(f'functions are {get_response}. \nGet Functions test completed successfully')
    tests_completed['get_functions'] = True
except Exception as msg:
    print(f'FAILED STEP: {msg}\nFailed get functions test')


"""-------------------------------CONSTANTS (GLOBAL SCOPE) DEMO------------------------
Usage:
3. (X) Get Constants
------------------------------------------------------------------------------------"""
tests_completed['get_constants'] = False
# 3. Sample Usage Module: Get Constants
try:
    get_response = constants.get_constants(credentials=credentials, entity_type_name='shraddha_test_1151_1')
    print(f'constants are {get_response}. \nGet Constants test completed successfully')
    tests_completed['get_constants'] = True
except Exception as msg:
    print(f'FAILED STEP: {msg}\nFailed get constants test')


"""-------------------------------SUMMARY OF TESTS------------------------
1. entitytype tests
2. functions tests
3. constants tests
------------------------------------------------------------------------"""
print('Summary of all tests run')
for name, status in tests_completed.items():
    print(f'Test {name} status {status}')