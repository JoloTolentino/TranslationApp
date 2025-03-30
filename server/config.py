from server.extensions import CONFIG


BAN_INTERVAL = 5
DATE_FMT = "%Y-%m-%d %H:%M:%S"

class CONFIG:
    PG_user = CONFIG['POSTGRES']['USER']
    PG_pwd = CONFIG['POSTGRES']['PASSWORD']
    PG_users = CONFIG['POSTGRES']['USERS_TABLE']
    PG_port = CONFIG['POSTGRES']['PORT']
    PG_env_addr = CONFIG['POSTGRES']['ENV_ADDRESS']
    PG_DB = CONFIG['POSTGRES']['DB']

    CHROMA_COLLECTION = CONFIG['CHROMA']['COLLECTION']

    if PG_pwd:
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_user}:{PG_pwd}@{PG_env_addr}:{PG_port}/{PG_DB}' 
    else:
        SQLALCHEMY_DATABASE_URI=f'postgresql+psycopg2://{PG_user}@{PG_env_addr}:{PG_port}/{PG_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = CONFIG['APP']['SECRET']
