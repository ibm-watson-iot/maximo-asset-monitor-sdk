#  | * IBM Confidential
#  | * OCO Source Materials
#  | * 5737-M66
#  | * © Copyright IBM Corp. 2020
#  | * The source code for this program is not published or otherwise divested of its
#  | * trade secrets, irrespective of what has been deposited with the U.S.
#  | * Copyright Office.

import sys
sys.path.insert(0, 'src')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# =============================================================================
# Convert README.md to README.rst for pypi
# Need to install both pypandoc and pandoc
# - pip insall pypandoc
# - https://pandoc.org/installing.html
# =============================================================================
# try:
#     from pypandoc import convert
#
#     def read_md(f):
#         return convert(f, 'rst')
# except:
#     print('Warning: pypandoc module not found, unable to convert README.md to RST')
#     print('Unless you are packaging this module for distribution you can ignore this error')
#
#     def read_md(f):
#         return "Python SDK for IBM Maximo Asset Monitor"

setup(
    name='mam-sdk',
    version="0.0.0",
    author='Shraddha Singh',
    author_email='shraddha.singh@ibm.com',
    package_dir={'': 'src'},
    packages=[
        'mam',
        'mam.sdk',
    ],
    #namespace_packages=['mam'],
    #package_data={'mam.sdk': ['*.pem']},
    # scripts=[
    #     'bin/mam-cli'
    # ],
    url='https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk',
    #license=open('LICENSE').read(),
    description='Python SDK for IBM Maximo Asset Monitor',
    # long_description=read_md('README.md'),
    install_requires=[
        "jsonschema >= 3.2.0",
        "iotfunctions @ git+https://github.com/ibm-watson-iot/functions.git@production#egg=iotfunctions"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
