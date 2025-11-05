from flask import Flask
from application.database import db #4 


from flask_login import LoginManager, UserMixin

app = None

def create_app():
    app = Flask(__name__) # consider this module app.py as the server code
    app.debug = True  # we do not need to run the code again it will automatically applies the changes.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.sqlite3" # 3 created the database with name parking name
    db.init_app(app)  #4 connecting db with app
    app.app_context().push() # it bring everything inside the context of flask application.if we dont write this it will throw runtime error
    app.secret_key = "smsokoamdqweweeewdnmsmdaqweef"

    return app



app = create_app()
from application.controllers import *  #2 emc


if __name__ == "__main__":
    app.run()
