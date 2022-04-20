from email.policy import default
from flask_login import UserMixin
from flaskauth import login_manager, db, app
from datetime import datetime, timedelta


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default="default.jpg")
    otp_val = db.relationship('Otp', backref='user', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        

class Otp(db.Model):
    __tablename__ = 'otp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    otp_value = db.Column(db.Integer, nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id') ,nullable=False)
    expired_datetime = db.Column(db.DateTime, nullable=False, default = datetime.now() + timedelta(minutes=5))
    auth_type = db.Column(db.String(50), default="From forget password")

    def __init__(self, otp_value, user_id, auth_type):
        self.otp_value = otp_value
        self.user_id = user_id
        self.auth_type = auth_type

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False, unique = True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
