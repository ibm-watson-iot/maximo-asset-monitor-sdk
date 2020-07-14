#!/usr/bin/env bash

# run this script ONLY ONCE
# it is IMPORTANT to do these two steps before running this script
#     1. activate the virtual environemnt (sets up $VIRTUAL_ENV)
#     2. run pip install PACKAGE (downloads drivers that we need to fix)
# fix is from https://github.com/ibmdb/python-ibmdb/issues/187#issuecomment-310765420


#path to virtual env
venv=$VIRTUAL_ENV
site_packages=$venv/lib/python*/site-packages
ibm_db=$site_packages/ibm_db*.*.so

fix_ibm_db(){
  #step 1
  install_name_tool -change libdb2.dylib $1/libdb2.dylib $2
  #step 2
  ln -s $1/clidriver/lib/libdb2.dylib $1/libdb2.dylib
  #step 3
  export DYLD_LIBRARY_PATH="$1/clidriver/lib:$1/clidriver/lib/icc"

  echo "fixed ibm_db setup for mac"
}


fail_msg="Sorry, something went wrong. Try the fix manually by following: https://github
.com/ibmdb/python-ibmdb/issues/187#issuecomment-310765420"

echo $fail_msg

echo $site_packages
echo $ibm_db

#for f in $ibm_db; do
#    ## Check if the glob gets expanded to existing files.
#    ## If not, f here will be exactly the pattern above
#    ## and the exists test will evaluate to false.
#    [ -e "$f" ] && fix_ibm_db $site_packages $ibm_db || echo $fail_msg
#    break
#done

