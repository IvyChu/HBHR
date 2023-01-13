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

