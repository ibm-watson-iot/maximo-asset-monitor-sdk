#!/usr/bin/env bash

# run this script ONLY ONCE
# it is IMPORTANT to do these two steps before running this script
#     1. activate the virtual environemnt (sets up $VIRTUAL_ENV)
#     2. run pip install PACKAGE (downloads drivers that we need to fix)
# fix is from https://github.com/ibmdb/python-ibmdb/issues/187#issuecomment-310765420


#path to virtual env
venv=$VIRTUAL_ENV
path_to_site_packages=$venv/lib/python*/site-packages
path_to_ibm_db=$site_packages/ibm_db*.*.so

get_ibm_db(){
  #pre-step
  echo "retrieving ibm_db cpython name" 
  cd "$1"
  ret_0=$?
  echo "command status $ret_0"
  ibm_db=ibm_db*.*.so
}

fix_ibm_db(){
  #pre-step
  echo "changing directory" 
  cd "$1"
  #step 1
  echo "running command" 
  echo "install_name_tool -change libdb2.dylib $1/libdb2.dylib $2"
  install_name_tool -change libdb2.dylib $1/libdb2.dylib $2
  ret_1=$?
  echo "command status $ret_1"
  #step 2
  echo "running command"
  echo "ln -s clidriver/lib/libdb2.dylib libdb2.dylib"
  ln -s clidriver/lib/libdb2.dylib libdb2.dylib
  ret_2=$?
  echo "command status $ret_2"
  #step 3
  echo "running command"
  echo "export DYLD_LIBRARY_PATH=$1/clidriver/lib:$1/clidriver/lib/icc"
  export DYLD_LIBRARY_PATH="$1/clidriver/lib:$1/clidriver/lib/icc"
  ret_3=$?
  echo "command status $ret_3"
}

get_ibm_db $path_to_site_packages
fix_ibm_db $path_to_site_packages $ibm_db
fail_msg="Sorry, something went wrong. Try the fix manually by following: https://github.com/ibmdb/python-ibmdb/issues/187#issuecomment-310765420"
success_msg="fixed ibm_db setup for mac"

if [[ $ret_1 -eq 0 &&  $ret_2 -eq 0  && $ret_3 -eq 0 ]]; then
  echo "$success_msg";
else
  echo "$fail_msg";
fi

echo $path_to_site_packages
echo $ibm_db
