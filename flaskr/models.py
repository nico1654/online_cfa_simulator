from flaskr import db, login_manager
from flask_login import UserMixin

# caricamento dell'utente corrente per il login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Classe User per la creazione del modello corrente nel database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    p_bucks = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.p_bucks}')"