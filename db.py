# Pylance suppressed warnings for imports
from app import app  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from os import getenv

# Initializes the PostgreSQL database


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
