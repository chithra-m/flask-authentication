from flask import Blueprint
from flask import render_template, request, session, current_app
from datetime import timedelta
from flaskauth.model import Post, Users, Role
from flaskauth import db, bcrypt

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if not Users.query.filter_by(email = "chithracse18@gmail.com").first():
        user = Users(
                username = "chithra",
                email = "chithracse18@gmail.com",
                password = bcrypt.generate_password_hash("Chithra@123"),
                role_id = 1
            )                                                  
        db.session.add(user)
        db.session.commit()
        print("inside")
    print("inside")
    return render_template('home.html', posts = posts)


@main.before_request
def before_request():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=1)