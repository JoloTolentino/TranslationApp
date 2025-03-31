from server.extensions import CFG


BAN_INTERVAL = 5
DATE_FMT = "%Y-%m-%d %H:%M:%S"

class CONFIG:
    PG_user = CFG['POSTGRES']['USER']
    PG_pwd = CFG['POSTGRES']['PASSWORD']
    PG_users = CFG['POSTGRES']['USERS_TABLE']
    PG_port = CFG['POSTGRES']['PORT']
    PG_env_addr = CFG['POSTGRES']['ENV_ADDRESS']
    PG_DB = CFG['POSTGRES']['DB']

    CHROMA_COLLECTION = CFG['CHROMA']['COLLECTION']

    SIGNUP_SCHEMA = CFG['SCHEMA_PATHS']['SIGNUP_VALIDATION']
    SUBSCRIPTION_SCHEMA = CFG['SCHEMA_PATHS']['SUBSCRIPTION_VALIDATION']
    USER_SCHEMA = CFG['SCHEMA_PATHS']['USER_VALIDATION']

    if PG_pwd:
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_user}:{PG_pwd}@{PG_env_addr}:{PG_port}/{PG_DB}' 
    else:
        SQLALCHEMY_DATABASE_URI=f'postgresql+psycopg2://{PG_user}@{PG_env_addr}:{PG_port}/{PG_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = CFG['APP']['SECRET']
