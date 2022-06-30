import logging
from datetime import datetime
from db.db_classes import (
    Physicians, Appointments, DB
)
from pony.orm.core import db_session, select, desc, flush, count, \
    max as pony_max, Query, Decimal
from typing import Dict, List, Union, Tuple


class DBActions:
    def __init__(self):
        self.obj_object = Physicians


    @db_session
    def get_physician(self, id: int, raw: bool = False):

        obj = self.obj_object.get(id=id)
            
        if obj:
            return self._db_obj_to_dict(obj, raw)

        return None

    @db_session
    def list_physicians(self, page: int = None, page_size: int = None, raw: bool = False):

        query = self.obj_object.select()
        
        if page and page_size:
            query = query.page(page, page_size)

        return self._query_to_dict(query, raw)

    @db_session
    def get_appointment(self, id: int, raw: bool = False):

        obj = Appointments.get(id=id)
            
        if obj:
            return self._db_obj_to_dict(obj, raw)

        return None

    @db_session
    def list_appointments(self, page: int = None, page_size: int = None, raw: bool = False):

        query = Appointments.select()
        
        if page and page_size:
            query = query.page(page, page_size)

        return self._query_to_dict(query, raw)

    @db_session
    def retrieve_appointments(self, physician_id: int, raw: bool = False):

        query = select(a for a in Appointments if a.physician_id.id == physician_id)
            
        if query:
            return self._db_obj_to_dict(query, raw)

        return None

    @staticmethod
    def _db_obj_to_dict(
            obj, raw: bool = False, dt_str: str = '%Y-%m-%d %H:%M:%S.%f'
    ) -> Union[Dict, None]:

        if raw:
            return obj

        if obj is None:
            return None

        dict_obj = obj.to_dict()
        for k, v in dict_obj.items():
            if type(v) == datetime:
                dict_obj[k] = datetime.strftime(v, dt_str)
            elif type(v) == Decimal:
                dict_obj[k] = float(v)

        return dict_obj

    def _query_to_dict(
            self, obj: Query, raw: bool = False,
            dt_str: str = '%Y-%m-%d %H:%M:%S.%f'
    ) -> List[Dict]:
        """
        Useful for a DBActions class to return either the raw PonyORM object,
        or a dictionary/list of dictionaries when the object contains datetime
        objects.
        :param entities: PonyORM Query object
        :param raw: if True, return the raw PonyORM object; otherwise,
        translate to Python dictionary/list of dictionaries
        :param dt_str: datetime format string to use when converting datetime
        object to a string
        :return: either the raw PonyORM object or the Python conversion
        """
        if raw:
            return obj[:]

        dict_list = []
        for o in obj:
            dict_obj = self._db_obj_to_dict(o, dt_str=dt_str)
            dict_list.append(dict_obj)

        return dict_list
