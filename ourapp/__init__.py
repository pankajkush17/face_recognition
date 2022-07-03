from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
from flask_login import LoginManager


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#db Config
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'


#Login manager init
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

#Sql db init
db = SQLAlchemy(app)
db.app = app


#importing our packages
from ourapp.users.routes import users
from ourapp.lofo.routes import lofo
from ourapp.attendance.routes import attendance

#registering the blueprint for our packages
app.register_blueprint(users)
app.register_blueprint(lofo)
app.register_blueprint(attendance)



