fichier = __file__.split("\\")[-1]
print(f"Loading {fichier}", flush=True, end=" : ")

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENV = "production"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'blabla-linux'
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
                                                            
print("ok")
