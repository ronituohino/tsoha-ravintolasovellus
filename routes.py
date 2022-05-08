from turtle import update
import icon
from app import app
from db import db
from flask import session, render_template, request, redirect, abort, flash
import account
from restaurant import (
    get_restaurant_by_id,
    get_groups,
    get_location,
    get_restaurant_ratings_by_id,
    translate_groups_to_id,
    update_average_rating,
)
from datetime import datetime
from search import (
    get_search_filter,
    get_group_filter,
    search_has_params,
    search_word_param,
    search_group_param,
)
import validation

# Defines the main routes for the application
@app.before_request
def before_request():
    # Get search bar groups
    sql = """SELECT id, name FROM groups"""
    result = db.session.execute(sql)
    groups = result.fetchall()
    serializable_groups = [{"id": g[0], "name": g[1]} for g in groups]
    session["groups"] = serializable_groups


@app.route("/")
def index():
    has_search = "search" in request.args
    has_groups = "groups" in request.args

    search_word = ""
    group_id_list = []
    group_count = 0
    if has_search:
        search_word = "".join(
            [f"%{word}%" for word in request.args["search"].split(" ")]
        )
    if has_groups:
        group_name_list = request.args["groups"].split("-")
        group_id_list = translate_groups_to_id(group_name_list)
        group_count = len(group_id_list)

    # Concatenating filters don't use input values, no SQL Injenction here
    filters = [
        get_search_filter(has_search),
        get_group_filter(has_groups),
    ]
    parsed_filters = [f for f in filters if f != None]
    string = "AND".join(parsed_filters)
    where_clause = ""
    if len(string) > 0:
        where_clause = "WHERE"

    # Connect filters and query the database
    sql = f"""SELECT id, name, description, address, phone, average_rating 
              FROM restaurants
              {where_clause} {string} 
              ORDER BY average_rating DESC"""
    result = db.session.execute(
        sql,
        {
            "search": search_word,
            "group_id_list": group_id_list,
            "group_count": group_count,
        },
    )
    restaurants = [
        {
            "id": r[0],
            "name": r[1],
            "description": r[2],
            "address": r[3],
            "phone": r[4],
            "average_rating": r[5],
        }
        for r in result.fetchall()
    ]
    print(restaurants)
    restaurant_amount = len(restaurants)
    id_list = [r["id"] for r in restaurants]

    # Find groups for each filtered restaurant
    restaurant_groups = get_groups(id_list)

    # Get restaurant location data in JSON format
    location_data = get_location(id_list)

    return render_template(
        "index.html",
        restaurants=restaurants,
        restaurant_amount=restaurant_amount,
        restaurant_groups=restaurant_groups,
        location_data=location_data,
    )


@app.route("/search", methods=["POST"])
def search():
    search_word = request.form["search"]
    has_search_word = len(search_word) > 0
    search_groups = request.form.getlist("groups")
    has_search_groups = len(search_groups) > 0

    params = [
        search_word_param(has_search_word, search_word),
        search_group_param(has_search_groups, search_groups),
    ]
    parsed_params = [p for p in params if p != None]
    string = "&".join(parsed_params)

    return redirect(f"/{search_has_params(parsed_params)}{string}")


@app.route("/restaurant/<int:id>", methods=["GET"])
def restaurant(id):
    restaurant = get_restaurant_by_id(id)
    ratings = get_restaurant_ratings_by_id(id)
    restaurant_groups = get_groups([id])

    # Get restaurant location data in JSON format
    location_data = get_location([id])

    return render_template(
        "restaurant.html",
        restaurant=restaurant,
        ratings=ratings,
        restaurant_groups=restaurant_groups,
        location_data=location_data,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Validation
        v = validation.Validator()
        v.check(v.not_empty("Käyttäjänimi", username))
        v.check(v.has_length_more_than("Käyttäjänimi", username, 3))
        v.check(v.not_empty("Salasana", password))
        v.check(v.has_length_more_than("Salasana", password, 5))
        if v.has_errors():
            flash(str(v))
            return redirect("/login")

        if account.login(username, password):
            return redirect("/")
        else:
            flash("Väärä tunnus tai salasana")
            return redirect("/login")


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

        # Validation
        v = validation.Validator()
        v.check(v.not_empty("käyttäjänimi", username))
        v.check(v.has_length_more_than("käyttäjänimi", username, 3))
        v.check(v.not_empty("salasana", password1))
        v.check(v.has_length_more_than("salasana", password1, 5))
        v.check(v.not_empty("salasana (uudestaan)", password2))
        if v.has_errors():
            flash(str(v))
            return redirect("/register")

        if password1 != password2:
            flash("Salasanat eroavat")
            return redirect("/register")
        if account.register(username, password1):
            return redirect("/")
        else:
            flash("Rekisteröinti epäonnistui, koska käyttäjänimi on jo käytössä")
            return redirect("/register")


@app.route("/give_rating", methods=["POST"])
def give_rating():
    if not account.check_csrf(request.form["csrf_token"]):
        abort(403)

    comment = request.form["comment"]
    rating = request.form["rating"]
    restaurant_id = request.form["restaurant_id"]
    account_id = account.account_session()["id"]

    # Validation
    v = validation.Validator()
    v.check(v.not_empty("kommentti", comment))
    v.check(v.has_length_less_than("Kommentti", comment, 200))
    v.check(v.not_empty("arvostelu", rating))
    v.check(v.is_value_between("Arvostelu", rating, 1, 5))
    v.check(v.not_empty("ravintola ID", restaurant_id))
    v.check(v.not_empty("käyttäjä ID", account_id))
    if v.has_errors():
        flash(str(v))
        return redirect(f"/restaurant/{restaurant_id}")

    # Error if this restaurant already has a rating from this user
    sql = """SELECT id FROM ratings WHERE account_id=:account_id AND restaurant_id=:restaurant_id"""
    result = db.session.execute(
        sql, {"account_id": account_id, "restaurant_id": restaurant_id}
    )
    existing_ratings = result.fetchall()
    if len(existing_ratings) > 0:
        flash("Arvostelun luonti epäonnistui, koska olet jo jättänyt arvostelun!")
        return redirect(f"/restaurant/{restaurant_id}")

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

    # Update restaurant average rating
    update_average_rating(restaurant_id)

    return redirect(f"/restaurant/{restaurant_id}")


@app.route("/delete_rating", methods=["POST"])
def delete_rating():
    if not account.check_csrf(request.form["csrf_token"]):
        abort(403)

    rating_id = request.form["rating_id"]
    restaurant_id = request.form["restaurant_id"]

    # Validation
    v = validation.Validator()
    v.check(v.not_empty("arvostelu ID", rating_id))
    if v.has_errors():
        flash(str(v))
        return redirect(f"/restaurant/{restaurant_id}")

    # Ratings can be deleted by admins, or by the user that made the rating
    if not account.require_admin():
        sql = """SELECT account_id FROM ratings WHERE id=:rating_id"""
        result = db.session.execute(sql, {"rating_id": rating_id})

        account_id = result.fetchone()
        if account_id[0] != account.account_session()["id"]:
            flash("Vaaditaan ylläpitäjä")
            return redirect(f"/restaurant/{restaurant_id}")

    # Validation
    v.check(v.not_empty("ravintola ID", restaurant_id))
    if v.has_errors():
        flash(str(v))
        return redirect(f"/restaurant/{restaurant_id}")

    sql = """DELETE FROM ratings WHERE id=:rating_id"""
    db.session.execute(sql, {"rating_id": rating_id})
    db.session.commit()

    update_average_rating(restaurant_id)

    return redirect(f"/restaurant/{restaurant_id}")


import routes_admin
