from namespaces.physicians import API
from classes.physicians import PhysiciansPath

API.add_resource(PhysiciansPath, "", methods=["GET"])