from flask import Flask
from flask import render_template, request, redirect
# Pylance suppressed warning for this import
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/test/index")
def index():
    words = ["apina", "banaani", "cembalo"]
    return render_template("test/index.html", message="Tervetuloa!", items=words)


@app.route("/test/pizza", methods=["POST"])
def result():
    pizza = request.form["pizza"]
    extras = request.form.getlist("extra")
    message = request.form["message"]
    return render_template("test/pizza.html", pizza=pizza,
                           extras=extras,
                           message=message)


@app.route("/test/database")
def database():
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("test/database.html", count=len(messages), messages=messages)


@app.route("/test/new")
def new():
    return render_template("/test/new.html")


@app.route("/test/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content": content})
    db.session.commit()
    return redirect("/test/database")


@app.route("/test/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)
