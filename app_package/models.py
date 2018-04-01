from app_package import db,app
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app_package import login
from flask_login import UserMixin
import jwt
import time

followers = db.Table('follwers',
    db.Column("follower_id",db.Integer,db.ForeignKey('user.id')),
    db.Column("followed_id",db.Integer,db.ForeignKey('user.id')))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(50), index=True, unique=True)
    aboutme = db.Column(db.String(400))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship("User",secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref("followers",lazy="dynamic"), lazy='dynamic')

    def __repr__(self):
        return "< user {}>".format(self.username)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    '''
        判断是否关注
    '''
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id==user.id).count() > 0

    '''
       关注用户
    '''
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    '''
        取消关注
    '''
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    '''
        获取关注用户以及自己的文章，发布时间倒序排列
    '''
    def followed_posts(self):
        # followed_post = Post.query.join("followers", 'followers.c.followed_id=Post.id').filter(followers.c.follower_id=self.id).order_by(Post.timestamp.desc())
        # return followed_post
        # 没有要 order by 
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
       
        own =  Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

        # followed = Post.query.join(
        #     followers, (followers.c.followed_id == Post.user_id)).filter(
        #         followers.c.follower_id == self.id)
        # own = Post.query.filter_by(user_id=self.id)
        # return followed.union(own).order_by(Post.timestamp.desc())
    
    def get_reset_password_token(self, expire_in=600):
        return jwt.encode({'reset_password':self.id,'exp':time.time()+expire_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")['reset_password']
        except:
            return
        return User.query.get(id)

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
