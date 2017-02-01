"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1,3])
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show all users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():
    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    """add new user to db"""
    email = request.form.get("username")
    password = request.form.get("password")
    count = User.query.filter_by(email=email).count()
    if count == 0:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("User sucsuccessfully added")
    else:
        flash("User already exists")
    return redirect("/")

@app.route("/login")
def login_form():
    email = request.args.get("l-username")
    password = request.args.get("l-password")
    // get user for user_id
    count = User.query.filter(email == email, password==password).count()
    if count != 0:
        flash("Sucsuccessfully login")
        session[]



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
