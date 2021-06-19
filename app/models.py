from . import db
from flask_login import current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(128))
  sname = db.Column(db.String(128))
  email = db.Column(db.String(128))
  profile_pic = db.Column(db.String())
  dataJoined = db.Column(db.DateTime, default=datetime.utcnow())
  pass_secure = db.Column(db.String(255))

  @property
  def password(self):
    raise AttributeError("You Can't Read the password attribute")

  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.pass_secure, password)

  def __repr__(self):
    return f'User {self.fname} {self.sname}'


class Blog(db.Model):
  __tablename__ = 'blog'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  content = db.Column(db.String())
  dateposted = db.Column(db.DateTime, default=datetime.utcnow())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
  users = db.relationship('User', backref='blog', lazy='dynamic')

  def save_pitch(self):
    db.session.add(self)
    db.session.commit()
  
  @classmethod
  def get_blogs_content(cls):
    return cls.query.all()

class Comment(db.Model):
  __tablename__ = 'comments'

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String(2000))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()
  
  @classmethod
  def get_specific_comment(cls, id):
    return cls.query.filter_by(pitch_id = id).all()