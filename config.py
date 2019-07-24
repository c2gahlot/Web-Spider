from os import environ


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI',
                                          'mysql+pymysql://root:root@localhost/web_spider')


class ProductionConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
