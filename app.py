"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def show_table():
    """show a list of users on screen"""

    return redirect('/users')

@app.route('/users')
def show_user_list():
    """show a list of users on screen"""

    users = User.query.all()


    return render_template("user_listing.html", users = users)

@app.route('/users/new')
def show_create_user_form():
    """show a form to create new user"""

    return render_template("create_user_form.html")

@app.route('/users', methods=["POST"])
def creat_new_users():
    """process the add form and adding new users to db
    redirect back to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def user_profile(user_id):

    return "hi"
