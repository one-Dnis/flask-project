from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SECRET_KEY'] = '0efddd00bcde7c335fe42093fc297f7c9f5fa0d2'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from cars import models, routes
