#  | * IBM Confidential
#  | * OCO Source Materials
#  | * 5737-M66
#  | * © Copyright IBM Corp. 2020
#  | * The source code for this program is not published or otherwise divested of its
#  | * trade secrets, irrespective of what has been deposited with the U.S.
#  | * Copyright Office.

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

"""-------------------------------SAMPLE USAGE------------------------
Usage:
1. Create entity type using a json payload
2. Load csv data for metrics 
3. Add dimension data using a json payload
4. Add kpi functions to Entity Type
5. Remove a kpi function
6. Remove a dimension
7. Delete entity type
------------------------------------------------------------------------"""

print("Sample Usecase Coming Soon!")