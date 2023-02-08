import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pathlib
import connexion

current_directory = os.path.abspath(os.path.dirname(__file__))

# Setting up a connexion flask app
basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

# Telling SQLAlchemy about the SQLite DB
sqlite_url = "sqlite:///" + os.path.join(current_directory, "mrv_emissions.db")

# Configure the SqlAlchemy part of the app instance
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create db
db = SQLAlchemy(app)

# Initialise Marshmallow
ma = Marshmallow(app)
