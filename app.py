from flask import Flask
from flask import render_template, request, redirect
# Pylance suppressed warning for this import
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    sql = "SELECT id, name, description, address FROM restaurants ORDER BY id DESC"
    result = db.session.execute(sql)
    restaurants = result.fetchall()
    return render_template("index.html", restaurants=restaurants)


@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = "SELECT id, name, description, address FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()
    return render_template("restaurant.html", restaurant=restaurant)
