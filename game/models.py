# database models 
from game import db, login_manager, app
from game import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

from flask_login import UserMixin
import datetime
from sqlalchemy.ext.declarative import declarative_base

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
 
 
 
class User(db.Model, UserMixin):
  id= db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(length=30), nullable=False, unique=True)
  email_address = db.Column(db.String(length=80), nullable=False, unique=True)
  password_hash = db.Column(db.String(length=60), nullable=False)
  links = db.relationship('Link', backref='owned_user', lazy=True) 
  rooms = db.relationship('Room', backref='owned_user', lazy=True) 

  
  def get_reset_token(self, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
    return s.dumps({'user_id': self.id}).decode('utf-8')
  
  @staticmethod
  def verify_reset_token(token):
    s = Serializer(app.config['SECRET__KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get(user_id)  
    
  
  
  @property
  def prettier_budget(self):
    if(len(str(self.budget)) >= 4):
      return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
    else:
      return f'{self.budget}'

      
  @property
  def password(self):
    return self.password
  
  @password.setter
  def password(self, plain_text_password):
    self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password.encode('utf-8'))  
  
  
class Link(db.Model):
  id= db.Column(db.Integer(), primary_key=True)
  created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
  original_url = db.Column(db.String(), nullable=False)
  clicks = db.Column(db.Integer(), nullable=True, default=0)
  owner = db.Column(db.Integer(), db.ForeignKey('user.id'), unique=True)  


   
  

class Room(db.Model):
  id= db.Column(db.Integer(), primary_key=True)
  created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
  room_name = db.Column(db.String(), nullable=False)
  clicks = db.Column(db.Integer(), nullable=True, default=0)
  owner = db.Column(db.Integer(), db.ForeignKey('user.id'), unique=True)  
  
  
  
  def __repr__(self):
    return f'{self.room_name}' 