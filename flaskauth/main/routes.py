from flask import Blueprint
from flask import render_template, request, session
from datetime import timedelta
from flaskauth import app
from flaskauth.model import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts = posts)


@main.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)