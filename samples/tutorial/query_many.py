# ------------------------------------------------------------------------------
# Copyright (c) 2017, 2022, Oracle and/or its affiliates.
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

# ------------------------------------------------------------------------------
# query_many.py (Section 3.3)
# ------------------------------------------------------------------------------

import oracledb
import db_config

con = oracledb.connect(user=db_config.user,
                        password=db_config.pw, 
                        dsn=db_config.dsn, 
                        config_dir=db_config.config_dir, 
                        wallet_location=db_config.wallet_location, 
                        wallet_password=db_config.wallet_password)

cur = con.cursor()

cur.execute("select * from dept order by deptno")
num_rows = 3
res = cur.fetchmany(num_rows)
print(res)

print(res[0])    # first row
print(res[0][1]) # second element of first row
