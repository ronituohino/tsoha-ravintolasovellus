from flask import Flask
from flask import render_template, send_file, request, redirect
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
    sql = "SELECT name, description, address FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()

    sql = "SELECT A.username, comment, rating, made_at FROM ratings R, accounts A WHERE restaurant_id=:id AND R.account_id=A.id"
    result = db.session.execute(sql, {"id": id})
    ratings = result.fetchall()
    print(ratings)
    return render_template("restaurant.html", restaurant=restaurant, ratings=ratings)


@app.route("/favicon.ico")
def favicon():
    return send_file("static/icon/favicon.ico", mimetype="image/x-icon")


@app.route("/apple-touch-icon.png")
def apple_favicon():
    return send_file("static/icon/apple-touch-icon.png", mimetype="image/png")


@app.route("/favicon-32x32.png")
def thirtytwo_favicon():
    return send_file("static/icon/favicon-32x32.png", mimetype="image/png")


@app.route("/favicon-16x16.png")
def sixteen_favicon():
    return send_file("static/icon/favicon-16x16.png", mimetype="image/png")


@app.route("/site.webmanifest")
def manifest():
    return send_file("static/icon/site.webmanifest")
