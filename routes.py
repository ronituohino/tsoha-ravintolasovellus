# Pylance suppressed warnings for imports
from app import app  # type: ignore
from db import db  # type: ignore
from flask import render_template

# Defines the main routes for the application


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

import icon  # type: ignore