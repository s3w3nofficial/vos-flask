from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_by_name

app = Flask(__name__)
app.config.from_object(config_by_name['dev'])
db = SQLAlchemy(app)