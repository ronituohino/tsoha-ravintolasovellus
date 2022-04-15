import icon
from app import app
from db import db
from flask import render_template, request, redirect, abort
import account
from restaurant import get_groups
from error import error
from datetime import datetime

# Defines the main routes for the application


@app.route("/")
def index():
    has_search = len(request.args) > 0
    if has_search:
        search_word = "".join(
            [f"%{word}%" for word in request.args["search"].split(" ")]
        )
        sql = """SELECT id, name, description, address
                 FROM restaurants WHERE name ILIKE :search OR description ILIKE :search 
                 ORDER BY id DESC"""
        result = db.session.execute(sql, {"search": search_word})
    else:
        sql = """SELECT id, name, description, address
                 FROM restaurants ORDER BY id DESC"""
        result = db.session.execute(sql)

    restaurants = result.fetchall()

    groups = get_groups(restaurants)

    return render_template("index.html", restaurants=restaurants, groups=groups)


@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = """SELECT id, name, description, address
             FROM restaurants WHERE id=:id"""
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()

    sql = """SELECT R.id, A.username, comment, rating, R.made_at, R.account_id
             FROM ratings R, accounts A
             WHERE restaurant_id=:id AND R.account_id=A.id"""
    result = db.session.execute(sql, {"id": id})
    ratings = result.fetchall()

    groups = get_groups([restaurant])

    return render_template(
        "restaurant.html", restaurant=restaurant, ratings=ratings, groups=groups
    )


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
            return error("Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    account.logout()
    return redirect("/")


@app.route("/search", methods=["POST"])
def search():
    search_word = request.form["search"]
    if len(search_word) > 0:
        return redirect(f"/?search={search_word}")
    else:
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
            return error("Salasanat eroavat")
        if account.register(username, password1):
            return redirect("/")
        else:
            return error("Rekisteröinti epäonnistui, käyttäjänimi on jo käytössä")


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
    db.session.execute(
        sql,
        {
            "comment": comment,
            "rating": rating,
            "restaurant_id": restaurant_id,
            "account_id": account_id,
            "made_at": made_at,
        },
    )
    db.session.commit()
    return redirect(f"/restaurant/{restaurant_id}")


@app.route("/delete_rating", methods=["POST"])
def delete_rating():
    if not account.check_csrf(request.form["csrf_token"]):
        abort(403)

    rating_id = request.form["rating_id"]

    if not account.require_admin():
        sql = """SELECT account_id FROM ratings WHERE id=:rating_id"""
        result = db.session.execute(sql, {"rating_id": rating_id})

        account_id = result.fetchone()
        if account_id[0] != account.account_session()["id"]:
            return error("Vaaditaan ylläpitäjä")

    restaurant_id = request.form["restaurant_id"]

    sql = """DELETE FROM ratings WHERE id=:rating_id"""
    db.session.execute(sql, {"rating_id": rating_id})
    db.session.commit()

    return redirect(f"/restaurant/{restaurant_id}")


import routes_admin
