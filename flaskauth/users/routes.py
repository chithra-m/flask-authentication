from flask import Blueprint
from flask import render_template, request, url_for, flash, redirect, session
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta, datetime
from flask_mail import Message
from flaskauth import bcrypt, db, app, mail, oauth
from flaskauth.users.forms import (RegistrationForm, LoginForm, AccountUpdateForm,
                             RequestResetForm, ResetPasswordForm, otpRequestForm)
from flaskauth.model import Users, Otp, Post
from sqlalchemy import desc
import pyotp
from flaskauth.users.utils import save_picture
import os

totp = pyotp.TOTP("base32secret3232")

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            
            flash(f'Account created for {form.username.data}!', 'success')
            user = Users(
                username = form.username.data,
                email = form.email.data,
                password = hashed_password
            )                                                   
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = Users.query.filter_by(email= form.email.data).first()
        
        if user is None:
            flash(f"{form.email.data} does not exist. Create an Acccount", 'danger' )
            return redirect(url_for('users.register'))

        elif form.email.data == user.email and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/delete_account/<email>")
def delete_account(email):
    try:
        if email:
            db.session.delete(Users.query.filter_by(email= email).first())
            db.session.commit()
        return "Deleted Successfully"
    except Exception as error:
        return "{email} does not exist."

@users.route('/google/')
def google():
    
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile', 
            # 'scope' : ' https://www.googleapis.com/auth/userinfo.profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('users.google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)


@users.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user_email = token['userinfo']['email']
    user = Users.query.filter_by(email= user_email).first()
        
    if user is None:
        flash(f"{user_email} does not exist. Create an Acccount", 'danger' )
        return redirect(url_for('users.register'))

    elif user_email == user.email :
        flash('You have been logged in!', 'success')
        login_user(user)
        return redirect(url_for('main.home'))

    return "error"


def generate_otp():
    otp_value = totp.now()
    # print(totp.verify(otp_value))
    return otp_value


def send_reset_email(user):
    # token = user.get_reset_token()
    otp_value = generate_otp()
    otp = Otp(
        otp_value = otp_value,
        user_id = user.id,
        auth_type=None
    )

    db.session.add(otp)
    db.session.commit()
           
    msg = Message('Password Reset Request',
                  sender="chithracse18@gmail.com",
                  recipients=[user.email])
    msg.body = f'''OTP value {otp_value}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
    return otp


@users.route("/reset_request", methods=['GET', 'POST'])
def reset_request():  
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.otp_validation',  user_email=user.email))

    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/otp_validation/<user_email>", methods=['GET', 'POST'])
def otp_validation(user_email):
    form = otpRequestForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=user_email).first()
        otp = Otp.query.filter_by(user_id = user.id).order_by(desc("id")).first()

        if (datetime.now() < otp.expired_datetime):
            if int(otp.otp_value) == int(form.otp.data):
                return redirect(url_for('users.reset_password', user_email = user_email))
        
    return render_template('otp.html', title='otp', form=form)


@users.route("/reset_password/<user_email>", methods=['GET', 'POST'])
def reset_password(user_email):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
   
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=user_email).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html', title='Reset Password', form=form)


@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    # try:
        form = AccountUpdateForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(f'Account updated', 'success')
            return redirect(url_for('main.home'))

        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email

        image_file = url_for('static', filename='profile_pics/' + current_user.image_file )
        return render_template('account.html', image_file=image_file, form = form)
    # except:
    #     return 'exception'
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)