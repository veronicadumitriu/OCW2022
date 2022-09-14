# ------------------------------------------------------------------------------
# create_user.py (Setup Section)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Copyright (c) 2022, Oracle and/or its affiliates.
#
# This software is dual-licensed to you under the Universal Permissive License
# (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl and Apache License
# 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose
# either license.
#
# If you elect to accept the software under the Apache License, Version 2.0,
# the following applies:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
import oracledb
import db_config_sys
import run_sql_script
import getpass
import os

# default values
PYTHON_USER = os.environ.get("PYTHON_USER", "pythondemo") 

#PYTHON_CONNECT_STRING = """(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-sanjose-1.oraclecloud.com))(connect_data=(service_name=g3f2a0f6aeefec7_db20220721220247_high.adb.oraclecloud.com))(security=(ssl_server_cert_dn="CN=adb.us-sanjose-1.oraclecloud.com, OU=Oracle ADB SANJOSE, O=Oracle Corporation, L=Redwood City, ST=California, C=US")))"""
#PYTHON_DRCP_CONNECT_STRING = """(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-sanjose-1.oraclecloud.com))(connect_data=(service_name=g3f2a0f6aeefec7_db20220721220247_high.adb.oraclecloud.com))(security=(ssl_server_cert_dn="CN=adb.us-sanjose-1.oraclecloud.com, OU=Oracle ADB SANJOSE, O=Oracle Corporation, L=Redwood City, ST=California, C=US"))):pooled"""

# dictionary containing all parameters; these are acquired as needed by the
# methods below (which should be used instead of consulting this dictionary
# directly) and then stored so that a value is not requested more than once
PARAMETERS = {}


def get_value(name, label, default_value=""):
    value = PARAMETERS.get(name)
    if value is not None:
        return value
    value = os.environ.get(name)
    if value is None:
        if default_value:
            label += " [%s]" % default_value
        label += ": "
        if default_value:
            value = input(label).strip()
        else:
            value = getpass.getpass(label)
        if not value:
            value = default_value
    PARAMETERS[name] = value
    return value


def get_main_user():
    return get_value("user", "Enter the User to be created", PYTHON_USER)


def get_main_password():
    return get_value("pw", "Enter the Password for %s" % get_main_user())


# Connect using the ADMIN User ID and password
con = oracledb.connect(user=db_config_sys.user,
                        password=db_config_sys.pw, 
                        dsn=db_config_sys.dsn, 
                        config_dir=db_config_sys.config_dir, 
                        wallet_location=db_config_sys.wallet_location, 
                        wallet_password=db_config_sys.wallet_password)
                        
# create sample user and schema
print("Creating user...")
run_sql_script.run_sql_script(con, "create_user", user=get_main_user(),
                              pw=get_main_password())
print("Done.")
