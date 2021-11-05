
from flask import Flask
from flask_pymongo import PyMongo
import flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app = flask.Flask(__name__)
#app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config['MONGO_URI'] = 'mongodb+srv://ben:Pakchk123@cluster0.9yvjr.mongodb.net/movie?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'

app.config['SECRET_KEY'] = 'process.env.SECRET_KEY'
app.config['MONGO_URI'] = 'process.env.MONGO_URI'
mongo = PyMongo(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    return users.find_one({'id': user_id})

from flaskblog import routes
