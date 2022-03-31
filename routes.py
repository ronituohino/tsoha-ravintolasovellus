# Pylance suppressed warnings for imports
import icon  # type: ignore
from app import app  # type: ignore
from db import db  # type: ignore
from flask import render_template, request, redirect, abort
import account  # type: ignore
from datetime import datetime

# Defines the main routes for the application


@app.route("/")
def index():
    sql = """SELECT id, name, description, address
             FROM restaurants ORDER BY id DESC"""
    result = db.session.execute(sql)
    restaurants = result.fetchall()
    return render_template("index.html", restaurants=restaurants)


@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = """SELECT id, name, description, address
             FROM restaurants WHERE id=:id"""
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()

    sql = """SELECT R.id, A.username, comment, rating, made_at
             FROM ratings R, accounts A
             WHERE restaurant_id=:id AND R.account_id=A.id"""
    result = db.session.execute(sql, {"id": id})
    ratings = result.fetchall()
    return render_template("restaurant.html", restaurant=restaurant, ratings=ratings)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if account.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    account.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if account.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti epäonnistui, käyttäjänimi on jo käytössä")


@app.route("/give_rating", methods=["POST"])
def give_rating():
    if not account.check_csrf(request.form["csrf_token"]):
        abort(403)

    comment = request.form["comment"]
    rating = request.form["rating"]
    restaurant_id = request.form["restaurant_id"]
    account_id = account.account_session()["id"]
    made_at = datetime.now()
    sql = """INSERT INTO ratings (comment, rating, restaurant_id, account_id, made_at) 
             VALUES (:comment, :rating, :restaurant_id, :account_id, :made_at)"""
    db.session.execute(sql, {"comment": comment, "rating": rating,
                       "restaurant_id": restaurant_id, "account_id": account_id, "made_at": made_at})
    db.session.commit()
    return redirect(f"/restaurant/{restaurant_id}")
