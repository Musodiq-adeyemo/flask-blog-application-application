from importlib.resources import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_mail import Mail,Message


app = Flask(__name__)

db = SQLAlchemy()

# This is the app configuration setting for flask-mail
app.config['MAIL_SERVER'] = 'smtp_mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] ="sirmuso@gmail.com"
app.config['MAIL_PASWORD'] ="********"

mail= Mail(app)

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'b6d504d64dd31e3d5eb1'
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, BlogPost

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))    

    from .main import main
    from .auth import auth
    
    # Blueprint registration
    app.register_blueprint(main,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    create_database(app)
    return app
# Database creation route
def create_database(app):
        db.create_all(app=app)
        print("database.db has been created")