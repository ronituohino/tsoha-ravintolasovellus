from db import db  # type: ignore
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

# Defines account functions


def login(username, password):
    sql = "SELECT id, password FROM accounts WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    account = result.fetchone()
    if not account:
        return False
    else:
        if check_password_hash(account.password, password):
            session["account"] = {
                "id": account.id,
                "username": username,
                "csrf_token": token_hex(16)
            }
            return True
        else:
            return False


def logout():
    del session["account"]


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO accounts (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def account_session():
    return session.get("account", 0)


def check_csrf(csrf):
    return account_session()["csrf_token"] == csrf
