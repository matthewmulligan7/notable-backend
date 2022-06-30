from flask import Blueprint
from flask_restx import Api
from resources.physicians import API as physicians
from resources.appointments import API as appointments

BLUEPRINT = Blueprint('apiv1', __name__, url_prefix='/api/v1')
API = Api(BLUEPRINT)

API.add_namespace(physicians)
API.add_namespace(appointments)
