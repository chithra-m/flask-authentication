import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
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
app.config['MAIL_USERNAME'] = "chithracse18@gmail.com"
app.config['MAIL_PASSWORD'] =  "Lekha@123"
mail = Mail(app)

app.config['RECAPTCHA_USE_SSL'] = True
app.config['RECAPTCHA_PUBLIC_KEY']='6LeyeCwfAAAAAPF5eLXYt67IokWQmMIXkFofRZn6'
app.config['RECAPTCHA_PRIVATE_KEY']='6LeyeCwfAAAAAGqkcsrKymQeKfQ_UyxXj6ynVO7e'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}
from flaskauth import routes


