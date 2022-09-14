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
import os
import getpass

# Tutorial credentials and connection string.
# Environment variable values are used, if they are defined.

user = os.environ.get("PYTHON_USER", "pythondemo")      #pythondemo schema, or your preferred schema when connecting to ADB
pw = os.environ.get("PYTHON_PASSWORD")
if pw is None:
    pw = getpass.getpass("Enter password for %s: " % user)

config_dir = os.environ.get("CONFIG_DIR") 
dsn = os.environ.get("DSN_ADB")
wallet_location = os.environ.get("WALLET_LOCATION")
wallet_password = os.environ.get("WALLET_PASSWORD")
if wallet_password is None:
    wallet_password = getpass.getpass("Enter password for the Wallet: " )
