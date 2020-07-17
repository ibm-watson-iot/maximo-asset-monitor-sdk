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

## How To Use

Examples for using the sdk modules are provided in ./scripts/sample_usage_script.py <br>

More to come

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

## Built With

* [NAME](http://www.dropwizard.io/1.0.2/docs/) - example link

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.