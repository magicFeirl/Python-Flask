from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from . import config

timezone = config.timezone
app.config.from_object(config.Config)

db = SQLAlchemy(app)

from . import model
from . import server

