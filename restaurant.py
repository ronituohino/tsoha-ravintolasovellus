from db import db  # type: ignore


def get_groups(restaurants):
    # Get group names as a list with restaurant id's
    id_list = [restaurant.id for restaurant in restaurants]
    sql = """SELECT C.restaurant_id, G.name FROM groups G, restaurant_group_connections C WHERE C.restaurant_id=ANY(:id_list) AND C.group_id=G.id"""
    result = db.session.execute(sql, {"id_list": id_list})
    groups = result.fetchall()
    return groups
