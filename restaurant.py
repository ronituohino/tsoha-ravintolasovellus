from db import db  # type: ignore
from const import months


def get_restaurant_by_id(id):
    sql = """SELECT id, name, description, address, phone
             FROM restaurants WHERE id=:id"""
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()
    return restaurant


def get_restaurant_ratings_by_id(id):
    sql = """SELECT A.username, comment, rating, R.account_id, R.made_at
             FROM ratings R, accounts A
             WHERE restaurant_id=:id AND R.account_id=A.id"""
    result = db.session.execute(sql, {"id": id})
    ratings = [
        {
            "username": c[0],
            "comment": c[1],
            "rating": c[2],
            "account_id": c[3],
            "made_at": format_time(c[4]),
        }
        for c in result.fetchall()
    ]
    return ratings


def format_time(time):
    return f"{time.day}. {months[time.month - 1]} - {time.year}"


def get_groups(restaurants):
    # Get group names as a list with restaurant id's
    id_list = [restaurant.id for restaurant in restaurants]
    sql = """SELECT C.restaurant_id, G.name FROM groups G, restaurant_group_connections C WHERE C.restaurant_id=ANY(:id_list) AND C.group_id=G.id"""
    result = db.session.execute(sql, {"id_list": id_list})
    return result.fetchall()


def get_location(restaurants):
    id_list = [restaurant.id for restaurant in restaurants]
    sql = """SELECT coords_lat, coords_lon, id, name FROM restaurants WHERE id=ANY(:id_list)"""
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
