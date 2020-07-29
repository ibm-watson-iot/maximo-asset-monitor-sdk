# Maximo Asset Monitor Python SDK

Maximo Asset Monitor(MAM) is used to visualize trends for devices and assets in customizable dashboards. This python
 sdk  will help users interact with the MAM APIs using python modules. With the provided modules, a user can:
 * create custom entity types, constants, functions, and metrics using a json payload
 * interact with entity types, constants, functions, and metrics
 * create metrics column using csv data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To use this application, you'll need python 3.7+ installed on your computer. Follow the instruction here to
 install the python on your machine https://www.python.org/downloads/
 

### Installing

Follow the step by step example to get the env running

**Step 1** Create a virtual environment
```
python3 -m venv env
```

**Step 2** Activate virtual environment
```
source env/bin/activate
```

**Step 3** Install sdk from github

```
pip install git+https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk.git
```

(*MacOS FIX*) if you are using MacOS and see ibm_db fails run the following command <br>
**NOTE**
* run this script ONLY ONCE
* it is IMPORTANT to do these two steps before running this script
    * (Step 2) activate the virtual environment (sets up $VIRTUAL_ENV)
    * (Step 3)run pip install PACKAGE (downloads the driver that we need to fix)
* fix is adopted from https://github.com/ibmdb/python-ibmdb/issues/187#issuecomment-310765420

```
bash ./dev_resources/mac_ibmdb_fix.sh
```

## Supported Modules
Module  | Description | Input | Output
--- | :---- | --- | ---
[create_custom_entitytype](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L85) | creates an entity type using json payload | `json_payload`[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_usage_data.json)<br/>`credentials` [getting credentials](#save-your-credentials-to-a-file) <br/> `**kwargs`<br/>{<br/>`drop_existing`  delete existing table and rebuild the entity type table in Db<br/>`db_schema` if no schema is provided will use the default schema<br/>} | None
[load_metrics_data_from_csv](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L201) | read metrics data for existing entity type | `entity_type_name` str name of entity type <br/>`file_path`[sample file](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_csv_data.csv)<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | None
[remove_entitytype](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L280) | delete entity type | `entity_type_name` str name of entity type <br/>`credentials`[getting credentials](#save-your-credentials-to-a-file)| api response
[add_functions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L48) | add kpi functions to an entity type |`json_payload`[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_function_data.json)<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | None
[get_functions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L109) | get all kpi functions for an entity type |`entity_type_name` str name of entity type <br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | list of dict with kpi functions (api response)
[remove_function](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L153) | delete a kpi functions from an entity type's functions |`entity_type_name` str name of entity type <br/>`kpi_name` str name of kpi function <br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | api response
[create_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L90) | register a constant (at global scope) | `json_payload`[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_constant_data.json)<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | api response
[get_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L147) | get all constants for a tenant | `entity_type_name` str name of entity type<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | list of dict with constants information (api response)
[update_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L175) | update constants for a tenant | `json_payload`[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_constant_data.json)<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | api response
[remove_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L229) | unregister constants by name |`constant_names` list of constant names to delete <br/>`credentials`[getting credentials](#save-your-credentials-to-a-file)  | api response
[add_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L66) | add dimension data for entities |`json_payload`[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_dimension_data.json)<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file)  | api response
[get_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L136) | get all the dimensional data for an entity type |`entity_type_name` str name of entity type <br/>`credentials`[getting credentials](#save-your-credentials-to-a-file)  | list of dict with dimension data information (api response)
[update_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L123) | update existing dimension data | `json_payload`:[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_dimension_data.json)<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file)  | api response
[remove_dimensions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L162) | delete dimension data by name | `dimension_names` list of dimension names to delete <br/>`entity_type_name`<br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | api response
[get_alerts](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/alerts.py#L51) | get all alerts using a json payload | `json_payload` [sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_alerts_data.json)  <br/>`credentials`[getting credentials](#save-your-credentials-to-a-file) | api response
[update_alert_status](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/alerts.py#L118) | update alert status using alert id | `alert_id` can get alert id using get_alerts <br/> `new_status` allowed values are: *New, Acknowledged, Resolved, Dismissed* <br/> `credentials`[getting credentials](#save-your-credentials-to-a-file) | None
[update_alert_severity](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/alerts.py#L157) | update alert severity using alert id | `alert_id` can get alert id using get_alerts <br/> `new_status` allowed values are *Low, Medium, High, Medium-High* <br/> `credentials`[getting credentials](#save-your-credentials-to-a-file) | None

## How To Use

### Save your credentials to a file

Set credentials to connect to Analytics Service.
* Create a credentials.json file in the scripts folder in your working directory. 
* On the user interface, go to the Services tab.
* Select Watson IoT Platform Analytics and click View Details.
* In the Environment Variables field, click Copy to Clipboard.
* Paste the contents of the clipboard into the credentials.json file.

Important: The credentials file is used to run or test the function locally. Do not push this file to your external repository

### Usage of sdk modules
Sample usage scripts 
* [creating entities, adding functions, constants, dimensions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_create_modules.py)
* [loading entity data from csv](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_load_csv_data.py)
* [removing entity type, functions, constants, dimensions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_delete_modules.py)
* [getting functions, constants, dimensions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_get_modules.py)
* [getting all alerts for entity type, updating alert status and severity](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_alerts_usage.py)

To interact with any module, we first need to load the credentials in our script
```python
credentials_path=<path to where you store credential.json in previous step>
with open(credentials_path, 'r') as F:
    credentials = json.load(F)
```
We can then call a module using this credentials and any other required/optional input
```python
entitytype.load_entitytype_data_from_csv('test_entity_type_name', csv_data_path, credentials=credentials)
```

