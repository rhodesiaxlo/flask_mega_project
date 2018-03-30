from app_package import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app_package import login
from flask_login import UserMixin



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(50), index=True, unique=True)
    aboutme = db.Column(db.String(400))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return "< user {}>".format(self.username)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return "< post {}> ".format(self.body)


@login.user_loader
def get_user(ident):
  return User.query.get(int(ident))
