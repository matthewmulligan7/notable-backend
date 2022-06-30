from pony.orm.core import QueryResult


def return_db_obj(obj, raw=False):
    """
    Useful for a DBActions class to return either the raw PonyORM object, or a dictionary/list of dictionaries.
    :param obj: PonyORM object
    :param raw: if True, return the raw PonyORM object; otherwise, translate to Python dictionary/list of dictionaries
    :return: either the raw PonyORM object or the Python conversion
    """
    if raw:
        return obj
    if isinstance(obj, (QueryResult, list)):
        return [o.to_dict() for o in obj]
    return obj.to_dict()


def catch_db_error(function):
    """
    Decorator to automatically capture a database error and return None if caught.
    :param function: decorated function
    :return: results of executed function, or None if exception caught
    """

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            return None

    return wrapper
