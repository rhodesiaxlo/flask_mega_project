from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)

# read config 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app_package import route, models