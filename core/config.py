import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = f"mysql+aiomysql://user:pw@db_url:3306/yourday"
    READER_DB_URL: str = f"mysql+aiomysql://user:pw@db_url:3306/yourday"
    JWT_SECRET_KEY: str = os.getenv("SECRET_KEY", "5dmhxb*_x9^acw+6zoi0e3!g_vlmkbc(^+at%fnp$44+7&^c")
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://admin:masterpassword@database-2.cztglubqcnqf.ap-northeast-2.rds.amazonaws.com:3306/yourday"
    READER_DB_URL: str = f"mysql+aiomysql://admin:masterpassword@database-2.cztglubqcnqf.ap-northeast-2.rds.amazonaws.com:3306/yourday"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"mysql+aiomysql://user:pw@db_url:3306/yourday"
    READER_DB_URL: str = f"mysql+aiomysql://user:pw@db_url:3306/yourday"


def get_config():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
