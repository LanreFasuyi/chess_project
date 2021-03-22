from game import app, db, mail, bcrypt 
from flask import render_template, redirect, url_for, request, flash

import chess
import chess.engine as CE
from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Message


from game.models import  User, Link, Room

from game.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, login_required, logout_user, login_required, current_user
import urllib.parse
from game.helpers import bcolors
from game import hasher

engine = CE.SimpleEngine.popen_uci("stockfish_12_win_x64\stockfish_12_win_x64.exe")



@app.route('/')
# @cross_origin()
def home():
   return render_template('index.html')

@app.route('/game', methods= ['POST'])
def generate_link():
  if request.method == "POST":
    url = request.form.get('user_id')
    user_id = url
    url = 'http://127.0.0.1/game/' + url
    if not url:
      flash("Something went wromg", category="danger")
      
      return redirect(url_for('home')) 
    
    check_link = Link.query.filter_by(owner=user_id).first()
    
    if check_link:
      url_id = check_link.id
      hashid = hasher.encode(url_id)
      short_url = request.host_url + 'game/' + hashid   
      return short_url
    else:  
      new_link = Link(original_url=url, owner=user_id) 
      db.session.add(new_link)
      db.session.commit()
      url_id = (new_link.id)  
      hashid = hasher.encode(url_id)
      short_url = request.host_url + 'game/' + hashid   
      return short_url
@app.route('/make_move', methods =['POST'])
# @login_required

def make_move():

   fen = request.form.get('fen')
   board = chess.Board(fen)
   
   #find best move
   result = engine.play(board, chess.engine.Limit(time=0.1))
   print(f'Result is {result}')

  
   #update internal python chess board state
   board.push(result.move)

   #extract FEN from curretn board state
   fen = board.fen()
   return {'fen': fen, 'best_move': str(result.move)}


@app.route('/game/<user>', methods= ['GET', 'POST'])
def startMultiPlay(user):
  # decode user 
  user_id =hasher.decode(user)
 
  
  
 
  # get user room 
  check_room = Room.query.filter_by(owner=1).first()
    
  if check_room:
    room = check_room.room_name
    # connect to the socket  
    # return room   
    return render_template('index.html', room=room)    

  else:  
    new_room = Room(room_name=user, owner=1) 
    db.session.add(new_room)
    db.session.commit()
    room_id = (new_room.id)  
    # return room_id
    return render_template('index.html', room=new_room.room_name)    
  # connect to socket 
  

@app.route('/register', methods=['GET', 'POST'])
def register_page():
  form = RegisterForm()
  if form.validate_on_submit():
    new_user= User(username=form.username.data, 
                   email_address= form.email_address.data, 
                   password = form.password1.data
                   )
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    flash(f'Account created succesfully! You are now logged in as {new_user.username}', category='success')


    return redirect(url_for('home'))    
    

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error: {err_msg}', category='danger')
  return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
  form = LoginForm()
  if form.validate_on_submit():
    attempted_user = User.query.filter_by(username=form.username.data).first()
    if attempted_user and attempted_user.check_password_correction(attempted_password= form.password.data):
      login_user(attempted_user)
      flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
      return redirect(url_for('home'))
    else:
      flash(f'Success! You are logged in as: {attempted_user.username}', category='danger')
 
  return render_template('login.html', form=form)



@app.route('/logout')
def logout():
  logout_user()
  flash('You have been logged out!', category='info')
  return redirect(url_for('home'))




def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message("Password Reset Request", sender="lanrefasuyii@gmail.com", recipients=[user.email_address])
  
  msg.body = f''' To reset your password, visit the following link:
  {url_for('reset_password', token=token, _external=True)}
  
  If you did not make this request, please ignore email
  '''

  mail.send(msg)

@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  
  form = RequestResetForm()
  
  if form.validate_on_submit():
    user = User.query.filter_by(email_address= form.email_address.data).first()
    send_reset_email(user)
    flash("An Email has been sent with reset instructions", category="info")
    return redirect(url_for('login_page'))
  return render_template('reset_request.html', title= 'Reset Password', form= form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('market'))
  user = User.verify_reset_token(token)
  if user is None:
    flash("The token is no longer valid", category="warning")
    return redirect(url_for('reset_request'))
  form = ResetPasswordForm()
  
  
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password1.data)
    user.password1 = hashed_password
    db.session.commit()

    flash(f'Your Password has been updated', category='success')
    
    return redirect(url_for('login_page'))


    return redirect(url_for('market'))
  
  
  return render_template('reset_password.html', title='Reset Password', form=form)


