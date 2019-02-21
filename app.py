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
def create_new_users():
    """process the add form and adding new users to db
    redirect back to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def user_profile(user_id):

    user = User.query.get(user_id)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template('user_detail.html', first_name=first_name, last_name=last_name, image_url=image_url, user_id=user_id)

@app.route('/users/<user_id>/edit')
def show_edit_user_profile(user_id):
    """Show form for editing user data"""

    user = User.query.get(user_id)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template('edit_user_form.html', first_name=first_name, last_name=last_name, image_url=image_url, user_id=user_id)

@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user_profile(user_id):
    """Edit the user profile based on the User ID"""

    user = User.query.get(user_id)

    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url') or None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user_profile(user_id):
    """Deletes the user profile"""

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
