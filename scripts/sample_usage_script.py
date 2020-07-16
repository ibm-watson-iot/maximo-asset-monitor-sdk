from mam.sdk import entitytype
import json

#DEFINE PATH TO REQUIRED FILES
#relative to where you run script from
credentials_path = './dev_resources/credentials.json'
data_path = './scripts/sample_usage_data.json'

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

# 1. Sample Usage Module: Create Entity Type
with open(data_path, 'r') as f:
    rc_create = entitytype.create_custom(f.read(), credentials=credentials)
    print(f'rc is {rc_create}. Create Entity Type test completed successfully')

# 2. Sample Usage Module: Delete Entity Type
with open(data_path, 'r') as f:
    data = json.load(f)
    rc_delete = entitytype.delete(data['entity_type_name'], credentials=credentials)
    print(f'rc is {rc_delete}. Delete Entity Type test completed successfully')
