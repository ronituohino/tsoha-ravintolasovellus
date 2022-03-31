# Pylance suppressed warnings for imports
from app import app  # type: ignore
from flask import send_file

# Defines routes for fetching icons


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
