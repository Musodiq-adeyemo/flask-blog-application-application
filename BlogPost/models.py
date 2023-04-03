from enum import unique
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(100),unique=True)
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    phone = db.Column(db.Integer())
    password1 = db.Column(db.String(20))
    password2 = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now())
    posts= db.relationship('BlogPost')
    images = db.relationship('Img')

    def __repr__(self):
        return f"User {self.username}"

class BlogPost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text(), nullable=False)
    author = db.Column(db.String(20),nullable=False)
    poster_id = db.Column(db.Integer())
    date_posted = db.Column(db.DateTime(timezone=True), server_default = func.now())
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __repr__(self):
        return f"BlogPost {self.title}"

class Img(db.Model):
    __tablename__='images'
    id = db.Column(db.Integer(), primary_key=True)
    img = db.Column(db.String(100),nullable = False)
    name = db.Column(db.String(500),nullable = False)
    mimetype = db.Column(db.String(500),nullable = False)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
