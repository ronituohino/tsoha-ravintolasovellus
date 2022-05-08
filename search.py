# Get request SQL Filters


def get_search_filter(has_search):
    if has_search:
        return "(name ILIKE :search OR description ILIKE :search)"
    return None


def get_group_filter(has_groups):
    if has_groups:
        return """R.id IN(SELECT restaurant_id FROM restaurant_group_connections 
                  WHERE group_id=ANY(:group_id_list) 
                  GROUP BY restaurant_id HAVING COUNT(*)=:group_count)"""
    return None


# Search url assembly


def search_has_params(params):
    if len(params) > 0:
        return "?"
    return ""


def search_word_param(has_search_word, search_word):
    if has_search_word:
        return f"search={search_word}"
    return None


def search_group_param(has_search_group, search_group):
    if has_search_group:
        return f"groups={'-'.join(search_group)}"
    return None
