from typing import Dict, List, Union
from common.utils import std_response, str_to_int
from db.db_actions import DBActions

class PhysiciansActions:
    def __init__(self):
        self.db_actions = DBActions()

    def retrieve_physicians(
            self, id: int = None, **kwargs
    ) -> Dict[Union[str, List[Dict], None], bool]:

        try:
            if id:
                obj = self.db_actions.get_physician(**kwargs)
            else:
                page, page_size = str_to_int(
                    kwargs.get('page'), kwargs.get('page_size')
                )
                obj = self.db_actions.list_physicians(page=page, page_size=page_size)

        except Exception as e:
            return std_response(
                f'ERROR caught trying to get obj: {e}', False
            )

        return std_response(obj, True)
