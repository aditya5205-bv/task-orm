import logging
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")


DB_CONFIG = {
    "user" : os.getenv('LOCAL_USER'), 
    "password" : os.getenv('LOCAL_PASSWORD'),
    "port" : os.getenv('LOCAL_PORT'),
    "database" : os.getenv('LOCAL_DB')
}

LOG_LEVEL = logging.INFO