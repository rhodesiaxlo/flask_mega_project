from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail

from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

# read config 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

login = LoginManager(app)
login.login_view = "login"

bootstrap = Bootstrap(app)
moment = Moment(app)


from app_package import route, models, error


# log 
if not app.debug:
    # 创建 log 文件
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler("logs/microblog.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')