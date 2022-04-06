from flask import render_template, request, url_for, flash, redirect, session
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta
from flask_mail import Message
from flaskauth import bcrypt, db, app, mail, oauth
from flaskauth.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flaskauth.model import Users
import os

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            # print(f"hashed data {hashed_password}")
            flash(f'Account created for {form.username.data}!', 'success')
            user = Users(
                username = form.username.data,
                email = form.email.data,
                password = hashed_password
            )                                                   
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = Users.query.filter_by(email= form.email.data).first()
        
        if user is None:
            flash(f"{form.email.data} does not exist. Create an Acccount", 'danger' )
            return redirect(url_for('register'))

        elif form.email.data == user.email and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route('/google/')
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
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    print(" Google User ", token)
    # user = oauth.google.parse_id_token(token)
    user_email = token['userinfo']['email']
    print(type(token))
    # print(userinfo)
    user = Users.query.filter_by(email= user_email).first()
        
    if user is None:
        flash(f"{user_email} does not exist. Create an Acccount", 'danger' )
        return redirect(url_for('register'))

    elif user_email == user.email :
        flash('You have been logged in!', 'success')
        login_user(user)
        return redirect(url_for('home'))

    return token


@app.route("/delete_account/<email>")
def delete_account(email):
    try:
        if email:
            db.session.delete(Users.query.filter_by(email= email).first())
            db.session.commit()
        return "Deleted Successfully"
    except Exception as error:
        return "{email} does not exist."
# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',
#                   sender="chithracse18@gmail.com",
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}

# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)


# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)


# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = Users.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)


