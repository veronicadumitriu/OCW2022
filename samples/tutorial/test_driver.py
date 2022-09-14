import oracledb
import db_config
import traceback
import os
import sys

oracledb.defaults.fetch_lobs = False  # fetch LOBs as string / bytes

#if sys.platform.startswith('darwin'):
#    oracledb.init_oracle_client(lib_dir=os.environ.get('HOME')+'/Downloads/instantclient_19_8')

un = os.environ.get('PYTHON_USERNAME')
pw = os.environ.get('PYTHON_PASSWORD')
cs = os.environ.get('PYTHON_CONNECTSTRING')

try:
    connection = oracledb.connect(user=db_config.user, password=db_config.pw, 
            dsn=db_config.dsn, config_dir=db_config.config_dir,
            wallet_location=db_config.wallet_location, wallet_password=db_config.wallet_password)

    with connection.cursor() as cursor:
        sql = """select systimestamp from dual"""
        for r in cursor.execute(sql):
            print(r)

except oracledb.Error as e:
    error, = e.args
    traceback.print_tb(e.__traceback__)
    print(error.message)

