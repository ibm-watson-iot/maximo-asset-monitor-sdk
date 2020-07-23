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

Step 1. Create a virtual environment
```
python3 -m venv env
```

Step 2. Activate virtual environment
```
source env/bin/activate
```

Step 3. Install sdk from github

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
[create_custom_entitytype](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L85) | creates an entity type using json payload | `json_payload`: [sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_usage_data.json)<br/><br/>`credentials`: local json file <br/><br/>**kwargs{`drop_existing`<br/>`db_schema`} | None
[load_metrics_data_from_csv](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L201) | read metrics data for existing entity type | `entity_type_name`<br/><br/>`file_path`<br/><br/>`credentials` | None
[remove_entitytype](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/entitytype.py#L280) | delete entity type | `entity_type_name`<br/><br/>`credentials`| None
[add_functions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L48) | add kpi functions to an entity type |`json_payload`:[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_function_data.json)<br/><br/>`credentials` |
[get_functions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L109) | get all kpi functions for an entity type |`entity_type_name`<br/><br/>`credentials` | 
[remove_function](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/kpifunction.py#L153) | delete a kpi functions from an entity type's functions |`entity_type_name`<br/><br/>`kpi_name`<br/><br/>`crednetials` | 
[create_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L90) | register a constant (at global scope) | `json_payload`:[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_constant_data.json)<br/><br/>`credentials` |
[get_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L147) | get all constants for a tenant | `entity_type_name`<br/><br/>`credentials` |
[update_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L175) | update constants for a tenant | `json_payload`:[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_constant_data.json)<br/><br/>`credentials` |
[remove_constants](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/constants.py#L229) | unregister constants by name |`constant_names`<br/><br/>`credentials`  |
[add_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L66) | add dimension data for entities |`json_payload`:[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_dimension_data.json)<br/><br/>`credentials`  |
[get_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L136) | get all the dimensional data for an entity type |`entity_type_name`<br/><br/>`credentials`  |
[update_dimensions_data](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L123) | update existing dimension data | `json_payload`:[sample payload](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/master/data/sample_dimension_data.json)<br/><br/>`credentials`  |
[remove_dimensions](https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk/blob/391a9eaacebc72fc9dd8a29a04705793c1579bb5/src/mam/sdk/dimension.py#L162) | delete dimension data by name | `dimension_names`<br/><br/>`entity_type_name`<br/><br/>`credentials` |

## How To Use

### Save your credentials to a file

Set credentials to connect to Analytics Service.
* Create a credentials_as.json file in the scripts folder in your working directory. On the user interface, go to
 the Services tab.
* Select Watson IoT Platform Analytics and click View Details.
* In the Environment Variables field, click Copy to Clipboard.
* Paste the contents of the clipboard into the credentials.json file.


Important: The credentials file is used to run or test the function locally. Do not push this file to your external repository

Examples for using the sdk modules are provided in ./scripts/sample_usage_script.py <br>

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```