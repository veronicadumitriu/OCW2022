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
# type_input_named_obj.py (Section 13.1)
# ------------------------------------------------------------------------------

import oracledb
import db_config_thick as db_config

con = oracledb.connect(user=db_config.user,
                        password=db_config.pw, 
                        dsn=db_config.dsn, 
                        config_dir=db_config.config_dir, 
                        wallet_location=db_config.wallet_location, 
                        wallet_password=db_config.wallet_password)

cur = con.cursor()

# Create table
cur.execute("""begin
                 execute immediate 'drop table testgeometry';
                 exception when others then
                   if sqlcode <> -942 then
                     raise;
                   end if;
               end;""")
cur.execute("""create table testgeometry (
               id number(9) not null,
               geometry MDSYS.SDO_GEOMETRY not null)""")

# Create a Python class for an SDO


class mySDO(object):

    def __init__(self, gtype, elemInfo, ordinates):
        self.gtype = gtype
        self.elemInfo = elemInfo
        self.ordinates = ordinates


# Get Oracle type information
obj_type = con.gettype("MDSYS.SDO_GEOMETRY")
element_info_type_obj = con.gettype("MDSYS.SDO_ELEM_INFO_ARRAY")
ordinate_type_obj = con.gettype("MDSYS.SDO_ORDINATE_ARRAY")

# Convert a Python object to MDSYS.SDO_GEOMETRY


def SDOInConverter(value):
    obj = obj_type.newobject()
    obj.SDO_GTYPE = value.gtype
    obj.SDO_ELEM_INFO = element_info_type_obj.newobject()
    obj.SDO_ELEM_INFO.extend(value.elemInfo)
    obj.SDO_ORDINATES = ordinate_type_obj.newobject()
    obj.SDO_ORDINATES.extend(value.ordinates)
    return obj


def SDOInputTypeHandler(cursor, value, numElements):
    if isinstance(value, mySDO):
        return cursor.var(oracledb.OBJECT, arraysize=numElements,
                          inconverter=SDOInConverter, typename=obj_type.name)


sdo = mySDO(2003, [1, 1003, 3], [1, 1, 5, 7])  # Python object
cur.inputtypehandler = SDOInputTypeHandler
cur.execute("insert into testgeometry values (:1, :2)", (1, sdo))

# Define a function to dump the contents of an Oracle object


def dumpobject(obj, prefix="  "):
    if obj.type.iscollection:
        print(prefix, "[")
        for value in obj.aslist():
            if isinstance(value, oracledb.Object):
                dumpobject(value, prefix + "  ")
            else:
                print(prefix + "  ", repr(value))
        print(prefix, "]")
    else:
        print(prefix, "{")
        for attr in obj.type.attributes:
            value = getattr(obj, attr.name)
            if isinstance(value, oracledb.Object):
                print(prefix + "  " + attr.name + " :")
                dumpobject(value, prefix + "    ")
            else:
                print(prefix + "  " + attr.name + " :", repr(value))
        print(prefix, "}")


# Query the row
print("Querying row just inserted...")
cur.execute("select id, geometry from testgeometry")
for (id, obj) in cur:
    print("Id: ", id)
    dumpobject(obj)
