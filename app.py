from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm
# from model import db, save_db
from base import app, bcrypt
from models.model import db, Users
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta

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


if __name__ == '__main__':
    app.run(debug=True)