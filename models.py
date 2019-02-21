"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.sql import func

DEFAULT_IMAGE_URL = "https://www.rithmschool.com/assets/team/whiskey-b19e7b9d17b43ac303323c552d46b3ddaf18d38ded9d10e4e1fa39f63c06622b.jpg"

ts = datetime.datetime.now().timestamp()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """This is a class for Users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(), default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """This is a class for Posts talbe"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="posts")
