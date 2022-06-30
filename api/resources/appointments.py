from namespaces.appointments import API
from classes.appointments import AppointmentsPath

API.add_resource(AppointmentsPath, "", methods=["GET"])