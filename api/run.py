from app.app import APP


with APP.app_context():
    #If the database flag is set import it
    from db import db_init
    db_init.init_db()


    #Import the api versions in context so app.config can exist later
    from api.v1.api_resources import BLUEPRINT as api_v1
    from api.v2.api_resources import BLUEPRINT as api_v2
    APP.register_blueprint(api_v1)
    APP.register_blueprint(api_v2)

application = APP

if __name__ == "__main__":
    APP.run(host="0.0.0.0")
    
    
