from flask_login import UserMixin

from application import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(128), nullable=True)
    bio = db.Column(db.String(256), nullable=True)
    profile_pic = db.Column(db.String(256), default="default.jpg")
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    following_users = db.relationship("Relation", foreign_keys="Relation.id_following", backref="following", lazy=True)
    follower_users = db.relationship("Relation", foreign_keys="Relation.id_follower", backref="follower", lazy=True)
    posts = db.relationship("Post", backref="posts_user", lazy=True)
    comments = db.relationship("Comment", backref="comments_user", lazy=True)
    likes = db.relationship("Like", backref="likes_user", lazy=True)

class Relation(db.Model):
    __tablename__ = "relationships"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=True)
    id_following = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_follower = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    relation_date = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.String(256), default="")
    photo = db.Column(db.String(256), nullable=False)
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    comments = db.relationship("Comment", backref="commented", lazy=True)
    likes = db.relationship("Like", backref="liked", lazy=True)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    commentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # comment_status = db.Column(db.Boolean, default=True)
    hidden = db.Column(db.Boolean, default=False)

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    status = db.Column(db.Boolean, default=True)
    like_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)