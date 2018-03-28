from flask import Flask
from config import Config

app = Flask(__name__)

# read config 
app.config.from_object(Config)

from app_package import route