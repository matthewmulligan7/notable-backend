from typing import Dict, List, Union
from common.utils import std_response, str_to_int
from db.db_actions import DBActions

class AppointmentsActions:
    def __init__(self):
        self.db_actions = DBActions()

    def retrieve_appointments(
            self, id: int = None, **kwargs
    ) -> Dict[Union[str, List[Dict], None], bool]:

        try:
            physician_id = kwargs["physician_id"]

            if physician_id:
                appointments = self.db_actions.retrieve_appointments(physician_id=physician_id)
            elif id:
                appointments = self.db_actions.get_appointment(**kwargs)
            else:
                page, page_size = str_to_int(
                    kwargs.get('page'), kwargs.get('page_size')
                )
                appointments = self.db_actions.list_appointments(page=page, page_size=page_size)

        except Exception as e:
            return std_response(
                f'ERROR caught trying to get obj: {e}', False
            )

        return std_response(appointments, True)
