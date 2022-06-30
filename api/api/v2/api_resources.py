from flask import Blueprint
from flask_restx import Api

BLUEPRINT = Blueprint('apiv2', __name__, url_prefix='/api/v2')
API = Api(BLUEPRINT)

