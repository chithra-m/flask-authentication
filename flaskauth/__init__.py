import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "your email"
app.config['MAIL_PASSWORD'] =  "email password"
mail = Mail(app)

app.config['RECAPTCHA_USE_SSL'] = True
app.config['RECAPTCHA_PUBLIC_KEY']='6LeyeCwfAAAAAPF5eLXYt67IokWQmMIXkFofRZn6'
app.config['RECAPTCHA_PRIVATE_KEY']='6LeyeCwfAAAAAGqkcsrKymQeKfQ_UyxXj6ynVO7e'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}
from flaskauth import routes


