import logging
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")

REDIS_CONN = {
    "host": os.getenv('REDIS_HOST'),
    "port": os.getenv("REDIS_PORT"),
    "decode_responses": os.getenv("DECODE_RESPONSES")
}

DB_CONFIG = {
    "user" : os.getenv('LOCAL_USER'), 
    "password" : os.getenv('LOCAL_PASSWORD'),
    "port" : os.getenv('LOCAL_PORT'),
    "database" : os.getenv('LOCAL_DB')
}

LOG_LEVEL = logging.INFO