from flask_restx import Resource, fields
from actions.physicians import PhysiciansActions
from flask import request
from common.utils import APILogger, APIResource, check_required
from namespaces.physicians import API as api
import json

fields = api.model(
    name="Capture data",
    model={
        "fields": fields.Raw(
            description="Fields", required=True
        ),
    },
)

class PhysiciansPath(APIResource):

    def __init__(self, ns):
        """
        Initialize class.
        :param ns: resource namespace context
        """
        super().__init__(ns)
        self.actions = PhysiciansActions()

    @APILogger
    def get(self, id: int = None) -> dict:

        return self.actions.retrieve_physicians(id=id, **request.args)
