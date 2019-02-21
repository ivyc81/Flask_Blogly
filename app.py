"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)
connect_db(app)
# db.create_all()

@app.route('/')
def show_table():
    """show a list of users on screen"""

    posts = Post.query.order_by(Post.created_at.desc())

    return render_template('homepage.html', posts=posts)

@app.route('/users')
def show_user_list():
    """show a list of users on screen"""

    users = User.query.all()

    return render_template("user_listing.html", users=users)

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

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def user_profile(user_id):

    user = User.query.get(user_id)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url
    posts = user.posts

    return render_template('user_detail.html', 
                           posts=posts, 
                           first_name=first_name, 
                           last_name=last_name, 
                           image_url=image_url, 
                           user_id=user_id)

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

@app.route('/users/<user_id>/posts/new')
def show_new_post_form(user_id):
    """Shows a new post for the user"""

    user = User.query.get(user_id)
    first_name = user.first_name
    last_name = user.last_name

    return render_template('new_post_form.html', first_name=first_name, last_name=last_name, user_id=user_id)

@app.route('/users/<user_id>/posts', methods=["POST"])
def create_new_post(user_id):
    """Creates a new post for the user"""

    title = request.form.get('title')
    content = request.form.get('content')

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<post_id>')
def show_post(post_id):
    """show post"""

    post = Post.query.get(post_id)
    title = post.title
    content = post.content
    user = post.user
    first_name = user.first_name
    last_name = user.last_name
    user_id = user.id

    return render_template("post_detail.html", title=title, content=content, first_name=first_name, last_name=last_name, user_id=user_id, post_id=post_id)

@app.route('/posts/<post_id>/edit')
def show_edit_post_form(post_id):
    """show a form for user to update post"""

    post = Post.query.get(post_id)
    title = post.title
    content = post.content

    return render_template('edit_post_form.html', title=title, content=content, post_id=post_id)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """update post"""

    post = Post.query.get(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')

    # db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """delete post"""

    post = Post.query.get(post_id)
    user = post.user
    user_id = user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

