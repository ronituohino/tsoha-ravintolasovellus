from db import db  # type: ignore
from const import months


def get_restaurant_by_id(id):
    sql = """SELECT id, name, description, address, phone, average_rating
             FROM restaurants WHERE id=:id"""
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()
    return restaurant


def get_restaurant_ratings_by_id(id):
    sql = """SELECT R.id, A.username, comment, rating, R.account_id, R.made_at
             FROM ratings R, accounts A
             WHERE restaurant_id=:id AND R.account_id=A.id"""
    result = db.session.execute(sql, {"id": id})
    ratings = [
        {
            "id": c[0],
            "username": c[1],
            "comment": c[2],
            "rating": c[3],
            "account_id": c[4],
            "made_at": format_time(c[5]),
        }
        for c in result.fetchall()
    ]
    return ratings


def format_time(time):
    return f"{time.day}. {months[time.month - 1]} - {time.year}"


def get_groups(id_list):
    # Get group names as a list with restaurant id's
    sql = """SELECT C.restaurant_id, G.name FROM groups G, restaurant_group_connections C WHERE C.restaurant_id=ANY(:id_list) AND C.group_id=G.id"""
    result = db.session.execute(sql, {"id_list": id_list})
    return result.fetchall()


def get_location(id_list):
    sql = """SELECT latitude, longitude, id, name FROM restaurants WHERE id=ANY(:id_list)"""
    result = db.session.execute(sql, {"id_list": id_list})
    location_data = result.fetchall()
    serializable_coords = [
        {"lat": l[0], "lon": l[1], "id": l[2], "name": l[3]} for l in location_data
    ]
    return serializable_coords


def translate_groups_to_id(group_name_list):
    # Turns list of group names to list of their id's
    sql = """SELECT id FROM groups WHERE name=ANY(:group_name_list)"""
    result = db.session.execute(sql, {"group_name_list": group_name_list})
    return [g[0] for g in result.fetchall()]


def update_average_rating(restaurant_id):
    sql = """SELECT AVG(rating) FROM ratings WHERE restaurant_id=:restaurant_id"""
    result = db.session.execute(sql, {"restaurant_id": restaurant_id})
    average_rating = result.fetchone()[0]

    if average_rating == None:
        average_rating = 0
    else:
        average_rating = round(average_rating, 1)

    sql = """UPDATE restaurants SET average_rating=:average_rating WHERE id=:restaurant_id"""
    db.session.execute(
        sql, {"average_rating": average_rating, "restaurant_id": restaurant_id}
    )
    db.session.commit()
