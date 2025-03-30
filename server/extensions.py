from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import configparser
import chromadb




db = SQLAlchemy()
chroma_client = chromadb.Client()
limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

formatter = logging.Formatter(logger_fmt)
file_handler = logging.FileHandler(f'./logs/{__name__}.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


error_handler = logging.FileHandler(f'./logs/{__name__}_errors.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(error_handler)



CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
