from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config_by_name

app = Flask(__name__)
app.config.from_object(config_by_name['dev'])
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)