from flask_restx import Resource, fields
from actions.appointments import AppointmentsActions
from flask import request
from common.utils import APILogger, APIResource, check_required
from namespaces.appointments import API as api
import json

class AppointmentsPath(APIResource):

    def __init__(self, ns):
        """
        Initialize class.
        :param ns: resource namespace context
        """
        super().__init__(ns)
        self.actions = AppointmentsActions()

    @APILogger
    @api.doc(
        params={
            "physician_id": "Get all appointments of physician_id",
        },
        validate=False,
    )
    def get(self, id: int = None) -> dict:

        return self.actions.retrieve_appointments(id=id, **request.args)

