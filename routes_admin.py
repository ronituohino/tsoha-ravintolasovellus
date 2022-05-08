from app import app
from db import db
from flask import render_template, request, redirect, abort, flash
import account
from datetime import datetime
import validation

# Defines the admin routes for the application


@app.route("/create_restaurant", methods=["GET", "POST"])
def admin_create_restaurant():
    if request.method == "GET":
        if not account.require_admin():
            flash("Vaaditaan ylläpitäjä")
            return redirect("/")
        else:
            sql = """SELECT id, name FROM groups"""
            result = db.session.execute(sql)
            groups = result.fetchall()
            return render_template("admin_create_restaurant.html", groups=groups)
    if request.method == "POST":
        if not account.check_csrf(request.form["csrf_token"]):
            abort(403)

        # Create restaurant
        name = request.form["name"]
        description = request.form["description"]
        address = request.form["address"]
        phone = request.form["phone"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        made_at = datetime.now()

        # Validation
        v = validation.Validator()
        v.check(v.not_empty("nimi", name))
        v.check(v.has_length_less_than("nimi", name, 50))

        v.check(v.not_empty("kuvaus", description))
        v.check(v.has_length_less_than("kuvaus", description, 200))

        v.check(v.not_empty("osoite", address))
        v.check(v.has_length_less_than("osoite", address, 50))

        v.check(v.not_empty("puhelinnumero", phone))
        v.check(v.has_length_less_than("puhelinnumero", phone, 12))

        v.check(v.not_empty("leveysaste", latitude))
        v.check(v.has_length_less_than("leveysaste", latitude, 10))

        v.check(v.not_empty("pituusaste", longitude))
        v.check(v.has_length_less_than("pituusaste", longitude, 10))

        if v.has_errors():
            flash(str(v))
            return redirect("/create_restaurant")

        sql = """INSERT INTO restaurants (name, description, address, phone, made_at, latitude, longitude, average_rating) 
                VALUES (:name, :description, :address, :phone, :made_at, :latitude, :longitude, :average_rating) RETURNING id"""
        result = db.session.execute(
            sql,
            {
                "name": name,
                "description": description,
                "address": address,
                "phone": phone,
                "made_at": made_at,
                "latitude": latitude,
                "longitude": longitude,
                "average_rating": 0,
            },
        )
        restaurant_id = result.fetchone()[0]

        # Create group listings
        groups = request.form.getlist("groups")
        for group in groups:
            sql = """INSERT INTO restaurant_group_connections (restaurant_id, group_id) VALUES (:restaurant_id, :group_id)"""
            db.session.execute(
                sql, {"group_id": int(group), "restaurant_id": restaurant_id}
            )

        db.session.commit()
        return redirect(f"/restaurant/{restaurant_id}")


@app.route("/delete_restaurant", methods=["POST"])
def admin_delete_restaurant():
    restaurant_id = request.form["restaurant_id"]

    if not account.require_admin():
        flash("Vaaditaan ylläpitäjä")
        return redirect(f"/restaurants/{restaurant_id}")

    if not account.check_csrf(request.form["csrf_token"]):
        abort(403)

    sql = """DELETE FROM restaurants WHERE id=:restaurant_id"""
    db.session.execute(sql, {"restaurant_id": restaurant_id})
    db.session.commit()
    return redirect("/")


@app.route("/create_group", methods=["GET", "POST"])
def admin_create_group():
    if request.method == "GET":
        if not account.require_admin():
            flash("Vaaditaan ylläpitäjä")
            return redirect("/")
        else:
            return render_template("admin_create_group.html")
    if request.method == "POST":
        if not account.check_csrf(request.form["csrf_token"]):
            abort(403)

        name = request.form["name"]

        # Validation
        v = validation.Validator()
        v.check(v.not_empty("nimi", name))
        v.has_length_less_than("nimi", name, 50)
        if v.has_errors():
            flash(str(v))
            return redirect("/create_group")

        sql = """INSERT INTO groups (name) VALUES (:name)"""
        result = db.session.execute(
            sql,
            {
                "name": name,
            },
        )
        db.session.commit()

        return redirect("/")
