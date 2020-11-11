from mam.sdk import (entitytype)
import json
import pandas as pd


#DEFINE PATH TO REQUIRED FILES
#relative to where you run script from
credentials_path = '../dev_resources/credentials.json'
csv_data_path = '../data/sample_csv_data.csv'

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

entitytype.load_metrics_data_from_csv('shradddha-boiler-test', csv_data_path, credentials=credentials)