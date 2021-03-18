from flask import Flask, render_template 
from flask_bcrypt import Bcrypt
import chess
import chess.engine as CE
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

engine = CE.SimpleEngine.popen_uci("stockfish_12_win_x64\stockfish_12_win_x64.exe")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_game.db'
app.config['SECRET_KEY'] = 'ceb5f71b06f4ab99bdf5b1a1'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from game import routes
