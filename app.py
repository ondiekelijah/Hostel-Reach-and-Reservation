#Comment lines 1-75 when inserting user roles and when creating a database using mirate
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_msearch import Search
# from .config import Config
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_cartegory = "info"
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
bcrypt = Bcrypt()
search = Search()

def create_app():
    app = Flask(__name__)
    app.secret_key = "67eadccda3bc198fangeluspaintissalife"
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+mysqlconnector://elie:dev123@localhost/hostel_reach"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['INFOKIT_ADMIN'] = "eochieng9448@gmail.com"

    login_manager.init_app(app)
    with app.app_context():
        db.init_app(app)
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    moment.init_app(app)
    bcrypt.init_app(app)
    search.init_app(app)

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    class MyModelView(ModelView):
        def is_accessible(self):
            # Change permissions here !!!
            access = current_user.is_authenticated 
            # and current_user.is_administrator()
            return access
        
    admin = Admin(app,name='Infokit Admin', template_mode='bootstrap3')
    from .models import User,Role
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Role, db.session))


    from .auth.routes import auth

    app.register_blueprint(auth)

    return app


# Use this to insert db roles
# Uncomment lines 80- 105 when inserting roles,comment the above
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# login_manager = LoginManager()
# login_manager.session_protection = "strong"
# login_manager.login_view = "auth.login"
# login_manager.login_message_cartegory = "info"
# db =SQLAlchemy()
# bcrypt = Bcrypt()


# def create_app():
#     app = Flask(__name__)
#     app.secret_key = '67eadccda3bc198fangelus'
#     app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://elie:dev123@localhost/blog'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     login_manager.init_app(app)

#     bcrypt.init_app(app)
#     db.init_app(app)

#     return app

# Inserting User roles
# Use these lines to avaoid "out of context" errors
# from app import create_app
# app = create_app()
# app.app_context().push()
# from models import Role
# from app import db
# Role.insert_roles()
# Role.query.all()

# [<Role 'User'>, <Role 'Moderator'>, <Role 'Administrator'>]
