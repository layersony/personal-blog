from . import db
from flask_login import current_user, UserMixin
from werkzeug import generate_password_hash, check_password_hash
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


