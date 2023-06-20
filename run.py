# Preparazione per la creazione dell'applicazione Flask
from flaskr import db, socketio
from flaskr.routes import app




if __name__ == '__main__':
    # Creazione delle tabelle
    with app.app_context():
        db.create_all()
    socketio.run(app, port=5000, host='192.168.1.129') 
    
    """_summary_
        TODO
        per lo sviluppo base dobbiamo finire di creare la pagina del gioco vero e proprio
        
        SVILUPPI FUTURI
        aggiungere un bot per permettere la partita single player
    """