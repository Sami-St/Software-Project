from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
session = Session()
login_manager = LoginManager()
secret_key = "3b1c60e954f646299c20e9c6b09a0b7d"


from models import User

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(User, int(user_id))

def create_app():

    app = Flask(__name__)

    db_file_path = '../software_projekt/datenbank/datenbank.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(db_file_path)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db

    db.init_app(app)
    bcrypt.init_app(app)
    session.init_app(app)
    login_manager.init_app(app)
    

    from routes import authentication, user_interactions
    app.register_blueprint(authentication)
    app.register_blueprint(user_interactions)

    login_manager.login_view = "authentication.login"

    # create tables defined in models.py in case they don't exist
    with app.app_context():
        db.create_all()

    # delete all rows in the specified table
    # from models import Klasse
    # with app.app_context():
    #     db.session.query(User).delete()
    #     db.session.commit()
    
    # delete specified table
    # from sqlalchemy import text
    # with app.app_context():
    #     with db.engine.connect() as connection:
    #         connection.execute(text('DROP TABLE IF EXISTS klasse'))

    return app
