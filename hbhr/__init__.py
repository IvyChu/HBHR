from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_mail import Mail

from flask_security import Security, SQLAlchemyUserDatastore

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

from hbhr.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

migrate = Migrate()

bcrypt = Bcrypt()

# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
mail = Mail()

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

# create a logger for the main app
log = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # more settings for logger
    log_dir = app.config['LOG_DIR']
    log.setLevel(logging.DEBUG)

    # create a file handler
    file_handler = logging.FileHandler(filename=f'{log_dir}hbhr-{datetime.datetime.now().strftime("%Y-%m")}.log')
    file_handler.setLevel(logging.DEBUG)

    # create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # add the file handler to the logger
    log.addHandler(file_handler)

    log.info('Logging set up!')

    log.debug(f"{app.config['SQLALCHEMY_DATABASE_URI']}")


    db.init_app(app)

    migrate.init_app(app, db)

           
    bcrypt.init_app(app)
    mail.init_app(app)
    talisman.init_app(app, content_security_policy=csp)

    

    # Setup Flask-Security
    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    from hbhr.users.routes import users
    from hbhr.main.routes import main
    from hbhr.admin.routes import admin
    from hbhr.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    return app