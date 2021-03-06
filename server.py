"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

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


@app.route("/users/<user_id>")
def show_user(user_id):
    """Return page showing the details of user."""

    print user_id
    user = User.query.get(user_id)
    print user
    print user.user_id
    print user.email
    print user.age
    print user.zipcode
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    user_rating = db.session.query(Rating.score, Movie.title).join(Movie).filter(Rating.user_id == user_id).all()
    print user_rating
    print len(user_rating)
    return render_template("user_details.html",
                           display_user=user,
                           display_user_rating=user_rating)

@app.route("/register", methods=["GET"])
def register_form():
    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """add new user to db"""
    email = request.form.get("username")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        flash("User sucsuccessfully added")
    else:
        flash("User already exists")
    return redirect("/")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""
    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login_form():
    #get user-provided email and password from request.form
    email = request.form.get("username")
    password = request.form.get("password")

    if "logged_in_user_id" not in session:
        session["logged_in_user_id"] = {}

    try:
        user = User.query.filter_by(email=email).one()
    except NoResultFound:
        flash("User is not found in our base")
        return redirect('/login')

    if password == user.password:
        session["logged_in_user_id"] = user.user_id
        print session
        flash("Login successful")
        route_to_user_id = '/users/' + str(user.user_id)
        return redirect(route_to_user_id)
    else:
        flash("Incorrect password")
        return redirect('/login')


@app.route("/logout")
def logout():
    session.pop('logged_in_user_id', None)
    flash('You were logged out')
    return redirect('/')



@app.route("/movies")
def movies_list():
    """Show all movies"""

    movies = Movie.query.order_by(Movie.title).all()
    print movies
    return render_template("movie_list.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Return page showing the details of movies."""

    print movie_id
    movie = Movie.query.get(movie_id)
    print movie
    print movie.movie_id
    print movie.title
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    movie_rating = db.session.query(Rating.score, User.email).join(User).filter(Rating.movie_id == movie_id).all()
    print movie_rating
    print len(movie_rating)
    return render_template("movie_details.html",
                           display_movie=movie,
                           display_movie_rating=movie_rating)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
