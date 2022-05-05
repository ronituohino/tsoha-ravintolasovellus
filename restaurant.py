from db import db  # type: ignore


def get_restaurant_by_id(id):
    sql = """SELECT id, name, description, address
             FROM restaurants WHERE id=:id"""
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()
    return restaurant


def get_restaurant_ratings_by_id(id):
    sql = """SELECT R.id, A.username, comment, rating, R.made_at, R.account_id
             FROM ratings R, accounts A
             WHERE restaurant_id=:id AND R.account_id=A.id"""
    result = db.session.execute(sql, {"id": id})
    ratings = result.fetchall()
    return ratings


def get_groups(restaurants):
    # Get group names as a list with restaurant id's
    id_list = [restaurant.id for restaurant in restaurants]
    sql = """SELECT C.restaurant_id, G.name FROM groups G, restaurant_group_connections C WHERE C.restaurant_id=ANY(:id_list) AND C.group_id=G.id"""
    result = db.session.execute(sql, {"id_list": id_list})
    groups = result.fetchall()
    return groups


def translate_groups_to_id(group_name_list):
    # Turns list of group names to list of their id's
    sql = """SELECT id FROM groups WHERE name=ANY(:group_name_list)"""
    result = db.session.execute(sql, {"group_name_list": group_name_list})
    return [g[0] for g in result.fetchall()]
