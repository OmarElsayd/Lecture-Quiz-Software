from sqlalchemy import create_engine

import sqlalchemy
import json


def get_db_config_file() -> dict:
    """
    Get db config file
    :return: dict with config
    """
    files_name = "lqs_database/db_models/db_config.json"
    with open(f'{files_name}') as config_file:
        return json.load(config_file)


def get_db_creds():
    """
    Get database creds
    :return:   user, password, host, port, database, schema od the database
    """
    config = get_db_config_file()
    if "database" not in config:
        raise KeyError("database object has to be in json config file")

    if "user" and "password" and "host" and "port" and "database" not in config["database"]:
        raise KeyError("database object must have user, password, host, port and database objects")

    db_creds = config["database"]

    user, password, host, port, database, schema = db_creds['user'], \
                                                   db_creds['password'], \
                                                   db_creds['host'], \
                                                   db_creds['port'], \
                                                   db_creds['database'], \
                                                   db_creds['schema']
    return user, password, host, port, database, schema


def create_db_engine() -> sqlalchemy.engine.create_engine:
    """
    Create database engine
    :return: sqlalchemy db engine
    """
    user, password, host, port, database, _ = get_db_creds()
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(url=url)
    return engine
