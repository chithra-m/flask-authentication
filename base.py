import os
import logging
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from model import db, app

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()
logging.info('Db tables created')