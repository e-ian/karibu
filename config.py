import os 
"""
module config to configure database
"""
class Config:
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/kaributest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    dbname = "kaributest"

class DevelopmentConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/kaributest'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig(Config):
    """
    class for testing configuration
    """
    DEBUG = False
    TESTING = True

class ProductionConfig(Config):
    """ production config class """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
