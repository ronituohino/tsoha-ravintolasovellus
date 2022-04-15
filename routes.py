# Pylance suppressed warnings for imports
import icon  # type: ignore
from app import app  # type: ignore
from db import db  # type: ignore
from flask import render_template, request, redirect, abort
import account  # type: ignore
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
    id_list = [restaurant.id for restaurant in restaurants]

    # Get group names as a list with restaurant id's
    sql = """SELECT C.restaurant_id, G.name FROM groups G, restaurant_group_connections C WHERE C.restaurant_id=ANY(:id_list) AND C.group_id=G.id"""
    result = db.session.execute(sql, {"id_list": id_list})
    groups = result.fetchall()

    return render_template("index.html", restaurants=restaurants, groups=groups)


@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = """SELECT id, name, description, address
             FROM restaurants WHERE id=:id"""
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()

    sql = """SELECT R.id, A.username, comment, rating, R.made_at
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


@app.route("/create_restaurant", methods=["GET", "POST"])
def admin_create_restaurant():
    if request.method == "GET":
        if not account.require_admin():
            return error("Vaaditaan ylläpitäjä")
        else:
            return render_template("admin_create_restaurant.html")
    if request.method == "POST":
        if not account.check_csrf(request.form["csrf_token"]):
            abort(403)

        name = request.form["name"]
        description = request.form["description"]
        address = request.form["address"]
        phone = request.form["phone"]
        made_at = datetime.now()

        sql = """INSERT INTO restaurants (name, description, address, phone, made_at) 
                VALUES (:name, :description, :address, :phone, :made_at) RETURNING id"""
        result = db.session.execute(
            sql,
            {
                "name": name,
                "description": description,
                "address": address,
                "phone": phone,
                "made_at": made_at,
            },
        )
        db.session.commit()

        restaurant_id = result.fetchone()[0]
        return redirect(f"/restaurant/{restaurant_id}")
