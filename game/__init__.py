import os
from flask import Flask 
from flask_bcrypt import Bcrypt
import chess
import chess.engine as CE
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from hashids import Hashids
from flask_cors import CORS
from flask_mail import Mail


engine = CE.SimpleEngine.popen_uci("stockfish_12_win_x64\stockfish_12_win_x64.exe")

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_game.db'
app.config['SECRET_KEY'] = 'ceb5f71b06f4ab99bdf5b1a1'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login_page'
login_manager.login_message_category= "info"


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

mail = Mail(app)




hasher= Hashids(min_length=4, salt=app.config['SECRET_KEY'])


from game import routes
