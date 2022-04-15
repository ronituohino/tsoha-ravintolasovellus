from flask import render_template

# A single function to render the error page with message


def error(message):
    return render_template("error.html", message=message)
