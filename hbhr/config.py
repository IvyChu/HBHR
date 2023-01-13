# -*- coding: utf-8 -*-
"""Config class sample

This is a sample file for the flask app configuration. Each environment
should have its own version of this renamed to config.py in the current
directory. The reason for doing it this way instead of using environment
variables to read the specific config is that app.config.from_envvar 
was not overwriting the settings read from the default configuration.
"""

import os


class Config(dict):
    # SECRET_KEY - random string used for security of the flask application
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # SQLALCHEMY_DATABASE_URI - this should be stored in the environment variable for security reasons
    SQLALCHEMY_DATABASE_URI = os.environ.get('HBHR_SQLALCHEMY_DATABASE_URI')

    # SQLALCHEMY_TRACK_MODIFICATIONS - disabled to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory where to store the log file - best if full path
    LOG_DIR = 'logs'
    
    # MAIL_SERVER - 'mail.carbld.com' on local machines and 'localhost' on the server
    MAIL_SERVER = 'mail.carbld.com'

    # MAIL settings - use SSL instead of TLS, port 465, put user and pass in env var
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = ('Carbld Support', 'support@carbld.com')

    # Directory where to store the log file - best if full path
    LOG_DIR = ''
