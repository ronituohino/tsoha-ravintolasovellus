from flask import Flask
from os import getenv

# Kicks off the Flask application


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
