from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_talisman import Talisman
from hbhr.config import Config
import logging
import datetime


convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
talisman = Talisman()

csp = {
    'default-src': [
        '\'self\'',
        '*.cloudflare.com',
        '*.googleapis.com',
        'https://bulma.io',
        'https://fonts.gstatic.com',
        'https://unpkg.com'
    ],
    'style-src': ['\'self\'',
        "'unsafe-inline'",
        'sha256-d7rFBVhb3n/Drrf+EpNWYdITkos3kQRFpB0oSOycXg4=',
        'https://bulma.io',
        'https://fonts.googleapis.com',
        '*.cloudflare.com'
    ],
    'script-src': ['\'self\'',
        '*.googleapis.com',
        '*.cloudflare.com',
        'https://unpkg.com'
    ]
}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    log_dir = app.config['LOG_DIR']

    # create a logger for the main app
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    # create a file handler
    file_handler = logging.FileHandler(filename=f'{log_dir}hbhr-{datetime.datetime.now().strftime("%Y-%m")}.log')
    file_handler.setLevel(logging.INFO)

    # create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # add the file handler to the logger
    log.addHandler(file_handler)

    logging.info('Logging set up!')


    db.init_app(app)

    migrate.init_app(app, db)
            
    bcrypt.init_app(app)
    #login_manager.init_app(app)
    talisman.init_app(app, content_security_policy=csp)

    from hbhr.users.routes import users
    from hbhr.admin.routes import admin
    from hbhr.main.routes import main
    from hbhr.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app