from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO, emit

# creazione dell'app flask e configurazione delle relative opzioni
app = Flask(__name__)
# impostazione della chiave segreta per la sicurezza dell'app
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# Impostazione dell'URI del database SQLite, occhio al triplo slash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

# Inizializzazione di SQLAlchemy, Bcrypt e LoginManager
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)  #inizializzo l' applicazione coi socket