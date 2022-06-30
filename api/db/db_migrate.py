from configparser import ConfigParser
import os
import pymysql
import json
from flask import current_app
from os import environ, listdir
from os.path import isfile 


def migrate_tables():

    dbkey = 'production'
    if os.environ.get('DEV'):
        dbkey = 'develop'

    # Get the database configurations
    config = ConfigParser(os.environ)
    config.read('db/db_config.ini')

    # Initialize the db if it's not in existence
    conn = pymysql.connect(
        host=config[dbkey]['dbhost'],
        user=config[dbkey]['dbuser'],
        password=config[dbkey]['dbpass'],
        port=int(config[dbkey]['dbport'])
    )

    try:
        for file in listdir('db/schemas/'): 
            if file.endswith('.json'): 
                schema_file = open('db/schemas/{}'.format(file))
                schema=json.loads(schema_file.read()) 

                try: 
                    with conn.cursor() as cursor:
                        # Execute the precheck statement, if it's None, do the alter
                        current_app.logger.info("Executing precheck for {}".format(file))
                        query = cursor.execute(schema['precheck'])
                        if query == 0:
                            current_app.logger.info("Proceeding to alter for {}".format(file))
                            for alter in schema['sql_statements']: 
                                cursor.execute(alter)
                except:
                    current_app.logger.info("Exception occurred in precheck {}".format(file))
    except: 
        current_app.logger.info("Exception occurred in executing alter checks")

    finally:
        conn.close()
