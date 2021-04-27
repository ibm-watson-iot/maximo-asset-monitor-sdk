---

copyright:
  years: 2017, 2019
lastupdated: "2019-06-18"

---

{:new_window: target="\_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}
{:child: .link .ulchildlink}
{:childlinks: .ullinks}

# Maximo Asset Monitor Python SDK
{: #python .reference}

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

Use the Python SDK to get started quickly with using the REST APIs of Maximo Asset Monitor. 
{:shortdesc}

Using the modules, you can interact with the REST APIs to:

- Manage entity types
- Manage dimensions
- Manage KPI functions
- Manage constants
- Load metric data


## Modules
{: #modules .sectiontitle}

Description | Module | Input | Output | Script
--- | :---- | --- | --- | --- 
Create an entity type using json payload |[create_custom_entity_type](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L85)  |<ul><li>`json_payload`: [See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_usage_data.json)</li><li>`credentials` : [See Adding credentials](#save-your-credentials-to-a-file)</li> <li>`**kwargs`<br/>{<br/>`drop_existing`: Delete existing table and rebuild the entity type table in the database<br/>`db_schema`: If no schema is provided, use the default schema<br/>}</li> </ul>| None | [Creating entities, adding functions, constants, dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_create_modules.py)
Read metric data for an existing entity type |[load_metrics_data_from_csv](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L201)  | <ul><li>`entity_type_name`: Name of entity type in string format </li><li>`file_path`: Path to the [file](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_csv_data.csv)</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul>| None | [Loading data from csv script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_load_csv_data.py)
Delete an entity type |[remove_entity_type](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L280) | <ul><li>`entity_type_name`: Name of entity type in string format</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul>| API response  | [Removing entity type, functions, constants, dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_delete_modules.py)
Add KPI functions to an entity type |[add_functions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L48) |<ul><li>`json_payload`: [See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_function_data.json)</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | None | [Creating entities, adding functions, constants, dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_create_modules.py)
Get all of the KPI functions of an entity type |[get_functions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L109) | <ul><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li><li>`entity_type_name`: Name of entity type in string format </li></ul>| List of dict with KPI functions (API response) | [Getting functions, constants, and dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_get_modules.py) 
Delete a KPI function of an entity type |[remove_function](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L153) |<ul><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li><li>`entity_type_name`: Name of entity type in string format</li><li>`kpi_name` Name of KPI function in string format<li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | API response | [Removing entity type, functions, constants, dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_delete_modules.py)
Register a constant globally |[create_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L90) |<ul><li>`json_payload`: [See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_constant_data.json)</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | API response | None
Get all of constants for a tenant |[get_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L147) |<ul><li> `entity_type_name` Name of entity type in string format</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file) </li></ul>| list of dict with constants information (API response) | [Get functions, constants, and dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_get_modules.py) 
Update constants for a tenant |[update_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L175) |<ul><li>`json_payload`[See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_constant_data.json)<li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li> </ul>| API response | None
Unregister constants by name |[remove_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L229) |<ul><li> `constant_names`: List of constant names to delete </li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | API response | None
Add dimension data to entities |[add_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L66) |<ul><li>`json_payload`: [See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_dimension_data.json)</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul>  | API response | [Creating entities, adding functions, constants, dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_create_modules.py)
Get all the dimensional data for an entity type |[get_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L136) | <ul><li>`entity_type_name` Name of entity type in string format <br/><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li> </ul>| List of dict with dimension data information (API response) | [Getting functions, constants, and dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_get_modules.py)
Update dimension data |[update_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L123)  | <ul><li>`json_payload`: [See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_dimension_data.json)<li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul>  | API response | None
Delete a dimension by name | [remove_dimensions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L162) | <ul><li>`dimension_names`: List of dimension names to delete </li></li>`entity_type_name`: Name of entity type in string format<li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | API response | [Removing entity type, functions, constants, dimensions script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_delete_modules.py)
Get all alerts using a json payload |[get_alerts](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/b331ed1e10b0ef6affc0c258334a05aa58a06e17/src/mam/sdk/alerts.py#L50) | <ul><li>`json_payload`: [See sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_alerts_data.json)</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | API response | [Get alerts and update status and severity script](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/scripts/sample_alerts_usage.py)
Update the alert status using the alert ID|[update_alert_status](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/b331ed1e10b0ef6affc0c258334a05aa58a06e17/src/mam/sdk/alerts.py#L117) |<ul><li> `alert_id`: Find the alert ID using the get_alerts method</li><li> `new_status`: Available values are *New, Acknowledged, Resolved, and Dismissed* </li> <li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul> | None | None 
Update the alert severity using alert ID |[update_alert_severity](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/b331ed1e10b0ef6affc0c258334a05aa58a06e17/src/mam/sdk/alerts.py#L156) |<ul><li>  `alert_id` Find the alert ID using the get_alerts method</li><li>`new_status`: Available values are *Low, Medium, and High*</li><li>`credentials`: [See Adding credentials](#save-your-credentials-to-a-file)</li></ul>| None | None 

## Installing the SDK
{: #install .sectiontitle}

Complete these steps to create a copy of the Python SDK and run it on your local system for development and testing purposes.

1. Create a virtual environment
    ```
    python3 -m venv env
    ```
2. Activate virtual environment
    ```
    source env/bin/activate
    ```
3. Install sdk from GitHub
    ```
    pip install git+https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk.git
    ```

On a MAS OS X environment, if the IBM database (ibm_db) fails, complete these steps:

1. Activate the virtual environment to set up the `$VIRTUAL_ENV` variable
    ```
    source env/bin/activate
    ```
2. Run the following command to download the driver:
    ```
    pip install git+https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk.git
    ```
3. Run the following command **once** to fix the driver:
    
    ```
    bash ./dev_resources/mac_ibmdb_fix.sh
    ```

For more information about the workaround, see https://github.com/ibmdb/python-ibmdb/issues/187#issuecomment-310765420

## Adding credentials to your script
{: #save-your-credentials-to-a-file .sectiontitle}

**Important**: The credentials file is used to run or test functions locally. Do not push this file to any external repository.

1. Set credentials to connect to Analytics Service.
   1. Create a credentials.json file in the scripts folder in your working directory. 
   2. On the user interface, go to the **Services** tab.
   3. Select Watson IoT Platform Analytics and click **View Details**.
   4. In the Environment Variables field, click **Copy to Clipboard**.
   5. Paste the contents of the clipboard into the credentials.json file.
2. Load your credentials in your script. Add the following code to your script:
    ```Python
    credentials_path=<path to credentials.json>
    with open(credentials_path, 'r') as F:
        credentials = json.load(F)
    ```
