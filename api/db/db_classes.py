from pony.orm import Database, PrimaryKey, Required, Set
DB = Database()


class ApiInfo(DB.Entity):
    id = PrimaryKey(int, auto=True)
    api_name = Required(str, 255)

class Physicians(DB.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    fname = Required(str, 256, unique=True)
    lname = Required(str, 256, unique=True)
    appointments = Set('Appointments', cascade_delete=True)

class Appointments(DB.Entity):
    id = PrimaryKey(int, auto=True, unsigned=True)
    physician_id = Required(Physicians)
    name = Required(str, 256, unique=True)
    time = Required(int, size=64)
    appointment_type = Required(str, 256)