from flask import g
import pymongo
import certifi
from app.config.config import load_config
import traceback
from app.utils.custom_logger import logger

def generate_database_connection_string(config_variables):
    username, password = config_variables['DB_USER'],config_variables['DB_PASSWORD']
    return f"mongodb+srv://{username}:{password}@cluster0.9jgzm.mongodb.net/?retryWrites=true&w=majority"

def connect_db():
    try:
        mongo_uri = generate_database_connection_string(load_config())
        client = pymongo.MongoClient(mongo_uri, tlsCAFile=certifi.where())
        client.admin.command("ping")
        g.mongo_client = client
    except Exception as e:
        logger.error("--------ERROR CONNECTION DB---------------")
        logger.error(e)
    return

def get_db():
    if 'mongo_client' not in g:
        connect_db()

    return g.mongo_client

def close_db_connection():
    db = g.pop("mongo_client", None)
    if db:
        logger.warning("Closing Database connection")
        db.close()
    return None
