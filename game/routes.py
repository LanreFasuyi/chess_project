from game import app, db 
from flask import render_template, redirect, url_for, request, flash

import chess
import chess.engine as CE
from flask import Flask, render_template, redirect, url_for, request

from game.models import  User

from game.forms import RegisterForm, LoginForm
from flask_login import login_user


engine = CE.SimpleEngine.popen_uci("stockfish_12_win_x64\stockfish_12_win_x64.exe")



@app.route('/')
def home():
   return render_template('index.html')

@app.route('/make_move', methods =['POST'])
def make_move():

   fen = request.form.get('fen')
   board = chess.Board(fen)
   
   #find best move
   result = engine.play(board, chess.engine.Limit(time=0.1))


   #update internal python chess board state
   board.push(result.move)

   #extract FEN from curretn board state
   fen = board.fen()
   return {'fen': fen, 'best_move': str(result.move)}




@app.route('/register', methods=['GET', 'POST'])
def register_page():
  form = RegisterForm()
  if form.validate_on_submit():
    new_user= User(username=form.username.data, 
                   email_address= form.email_address.data, 
                   password_hash = form.password1.data
                   )
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home'))    
    

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error: {err_msg}', category='danger')
  return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
  form = LoginForm()
  return render_template('login.html', form=form)