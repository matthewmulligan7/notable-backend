from configparser import ConfigParser
import os
import pymysql
from pony.flask import Pony
from flask import current_app as APP
from db.db_classes import DB
from . import db_migrate


def init_db():
    dbkey = 'production'
    if os.environ.get('DEV'):
        dbkey = 'develop'

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
        with conn.cursor() as cursor:
            if (cursor.execute('SHOW DATABASES LIKE "{}"'.format(config[dbkey]['dbname']))) == 0:
                cursor.execute('CREATE DATABASE {}'.format(
                    config[dbkey]['dbname']))
    finally:
        conn.close()
    
    DEBUG = True if 'DEBUG' in os.environ else False
    APP.config.update(dict(
        DEBUG=DEBUG,
        PONY={
            'provider': config[dbkey]['dbtype'],
            'user': config[dbkey]['dbuser'],
            'password': config[dbkey]['dbpass'],
            'host': config[dbkey]['dbhost'],
            'database': config[dbkey]['dbname'],
            'port': int(config[dbkey]['dbport']),
            'charset': 'utf8mb4'
        }))

    DB.bind(**APP.config['PONY'])
    APP.logger.info("Successfully connected to database")

    if os.environ.get('MIGRATE_TABLES') == "FALSE":
        APP.logger.info("MIGRATE_TABLES set to FALSE..skipping")
    else:
        db_migrate.migrate_tables()

    DB.generate_mapping(create_tables=True)
    Pony(APP)
