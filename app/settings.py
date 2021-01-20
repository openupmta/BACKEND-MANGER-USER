import os

os_env = os.environ


class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    # app config
    ENV = 'production'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = False

    JWT_SECRET_KEY = '1234567a@'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # SQL Alchemy config
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'new_website.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Development configuration."""
    # app config
    ENV = 'development'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = True
    # SQL Alchemy config

    # JWT Config
    JWT_SECRET_KEY = '1234567a@'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # SQL Lite
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'new_website.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Test configuration."""
    # app config
    ENV = 'test'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = False
    # SQL Lite
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'new_website.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
