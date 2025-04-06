from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import logging
import configparser
import chromadb
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db = SQLAlchemy()
chroma_client = chromadb.Client()
limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logs_dir = os.path.join(base_dir, "logs")

formatter = logging.Formatter(logger_fmt)
file_handler = logging.FileHandler(os.path.join(logs_dir, f"{__name__}.log"))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # Or INFO
stream_handler.setFormatter(formatter)

error_handler = logging.FileHandler(os.path.join(logs_dir, f"{__name__}_errors.log"))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(error_handler)
logger.addHandler(stream_handler)


CFG = configparser.ConfigParser()
CFG.read(os.path.join(base_dir, "config.ini"))
