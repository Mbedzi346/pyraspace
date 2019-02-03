from flask import Flask, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import os
import logging

app = Flask(__name__, static_url_path='/app/static')
app.config.from_object(Config)

app.config['MAIL_SERVER'] = 'oxenfurt.aserv.co.za'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'orders@pyraspace.com'
app.config['MAIL_PASSWORD'] = 'pyramarket83'  # pyrcleaaline365
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'register'
app.secret_key = os.urandom(24)

mail = Mail(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('Logs')

from app import models, routes


