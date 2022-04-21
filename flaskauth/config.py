import os

class Config:
    SECRET_KEY  = os.environ.get('SECRET_KEY')
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER  = 'smtp.gmail.com'
    MAIL_PORT  = 465
    MAIL_USE_TLS  = False
    MAIL_USE_SSL  = True
    MAIL_USERNAME  = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD  =  os.environ.get('EMAIL_PASS')

    RECAPTCHA_PUBLIC_KEY ='6LeyeCwfAAAAAPF5eLXYt67IokWQmMIXkFofRZn6'
    RECAPTCHA_PRIVATE_KEY ='6LeyeCwfAAAAAGqkcsrKymQeKfQ_UyxXj6ynVO7e'      
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_OPTIONS = {'theme':'black'}