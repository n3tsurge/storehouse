import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///storehouse.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///storehouse.db"    

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = "sqlite:///storehouse-dev.db"    

class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False    
    SQLALCHEMY_DATABASE_URI = "sqlite:///storehouse-test.db"    

app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}