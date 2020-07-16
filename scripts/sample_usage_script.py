from mam.sdk import entitytype
import json

#DEFINE PATH TO REQUIRED SETUP FILES
#relative to where you run script from
credentials_path = './dev_resources/credentials.json'
environment_path = './dev_resources/environment.json'

#LOADING DATABASE CREDENTIALS
'''
# Getting and saving Db credentials
# Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
# Paste contents in credentials.json file
# Save file in maximo-asset-monitor-sdk/dev_resources folder (one example)
'''
print('Reading Db Credentials')
with open(credentials_path, 'r') as F:
    credentials = json.load(F)

# LOADING API CREDENTIALS
'''
# Getting API credentials and Creating environment.json file
# Explore > Usage > Watson IOT Platform Services > Copy to api key
# Paste contents in `"valid-api-key-goes-here"` as shown in sample environment.json file
# Explore > Usage > Watson IOT Platform Services > Copy to api token
# Paste contents in `"valid-api-token-goes-here"` as shown in sample environment.json file
# Save file in maximo-asset-monitor-sdk/dev_resources folder (one example)

sample environment.json file:
{
  "tenant_id": "AnalyticsServiceDev",
  "_comment_tenant_id": "REQUIRED. same as the one credentials.json",

  "base_url": "https://api-dev.connectedproducts.internetofthings.ibmcloud.com",
  "_comment_base_url": "REQUIRED",
  
  "version": "v1",
  "_comment_version": "OPTIONAL. default value is v1",

  "isBasicAuth": false,
  "_comment_isBasicAuth_1/3": "REQUIRED. default value is false. ",
  "_comment_isBasicAuth_2/3": "when true requires: API_USERNAME and API_PASSWORD when True. ",
  "_comment_isBasicAuth_3/3": "when false requires: authentication_header={'x-api-key', 'x-api-token'}",
  
  "authentication_header": {
    "X-api-key": "valid-api-key-goes-here",
    "X-api-token": "valid-api-token-goes-here"
  },
  "_comment_authentication_header": "REQUIRED",

  "disableCertificateVerification": true,
  "_comment_disableCertificateVerification_1/1": "OPTIONAL. default value is true"
}
'''
print('Reading API Credentials')
with open(environment_path, 'r') as F:
    environment = json.load(F)

# 1. Sample Usage Module: Create Entity Type
with open('./local_test_data.json', 'r') as f:
    rc_create = entitytype.create_custom(f.read(),
                                         credentials=credentials,
                                         environment=environment)
    print(f'rc is {rc_create}. Create Entity Type test completed successfully')

# 2. Sample Usage Module: Delete Entity Type
with open('./local_test_data.json', 'r') as f:
    data = json.load(f)
    rc_delete = entitytype.delete(data['entity_type_name'])
    print(f'rc is {rc_delete}. Delete Entity Type test completed successfully')
