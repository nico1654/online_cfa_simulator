from flask import render_template, url_for, redirect, flash, session
from flaskr.forms import RegistrationForm, LoginForm
from flaskr.models import User
from flaskr import db, bcrypt
from flaskr import app, socketio
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import join_room, send, rooms, leave_room
from flaskr.pokerGame import PokerGame

active_rooms = {}
active_players = {}
poker_games = {}


# controllo dell evento nel socket
@socketio.on('change_color')
def test(data):
    print(data["current_room"], flush=True)
    print(rooms())
    print("\n\n\n", flush=True)
    socketio.emit("color", data["color"], to=data["current_room"])

#send the avaiable room when a new user enter the page
@socketio.on("startInfo")
def connect():
    socketio.emit("setup", active_rooms)

#create a new room
@socketio.on('join')
def on_join(data):
    username = current_user.username  
    room = username + "_" + data['room']  #create the room based on the username
    active_rooms[room] = username + ","
    #TODO delete the room from active rooms
    for room_name in rooms():
        leave_room(room_name)
        
    join_room(room)
    
    user_room = current_user.username
    active_players[current_user.username] = current_user.username
    join_room(user_room)
    
    send(username + ' has entered the room: ' + room, to=room)
    socketio.emit("load_avaiable_rooms", active_rooms, broadcast=True)
    socketio.emit("send_current_room", room, to=room)

#enter an existing room
@socketio.on('enter_existing_room')
def on_enter_existing_room(data):
    username = current_user.username
    room = data["room"]
    for room_name in rooms():
        leave_room(room_name)
    join_room(room)
    
    user_room = current_user.username
    active_players[current_user.username] = current_user.username
    join_room(user_room)
    
    active_rooms[room] += username + "," 
    print("entered room " + room, flush=True)
    
    send(username + ' has entered the room: ' + room, to=room)
    socketio.emit("send_current_room", room, to=room)

@socketio.on("leave_room")
def on_leave_current_room(data):
    rooms_to_eliminate = []
    for room_name, users in active_rooms.items():
        if current_user.username in users: #if user is inside the room he leve it
            leave_room(data["room"])
            active_rooms[room_name] = active_rooms[room_name].replace(current_user.username + ",", "")
            if active_rooms[room_name] == "":  #then i delete the room from active_rooms variable
                rooms_to_eliminate.append(room_name)
    for room_name in rooms_to_eliminate:  #eliminate every single empty room
        active_rooms.pop(room_name)
    socketio.emit("load_avaiable_rooms", active_rooms, broadcast=True) #load all room for all users


@socketio.on("start_game") #start the game for all user in the room
def on_start_game(data):
    socketio.emit("load_game_page", to=data["room"]) #tell all user in the room to load the new page
    number_of_players = len(active_rooms[data["room"]].split(",")) - 1
    poker_games[current_user.username] = PokerGame(number_of_players) #create the poker game for n player
    poker_games[current_user.username].start_game()
        

@socketio.on("give_cards") #give the cards for all users in the room
def on_give_cards(data):
    print(data, flush=True)
    curr_name = data.split("_room")[0]
    
    socketio.emit("show_table_cards", poker_games[curr_name].table_cards, to=current_user.username)
    
    player_index = active_rooms[data].split(",").index(current_user.username)  
    print(active_rooms[data].split(","), flush=True)
    print(active_rooms[data], flush=True)
    socketio.emit("show_cards",  poker_games[curr_name].players[player_index].hand, to=current_user.username)
    
    if current_user.username == data.split("_room")[0]: # give the turn to the first player
        socketio.emit("give_starting_turn",  [True, 100], to=current_user.username)
    else:
        socketio.emit("give_staring_turn",  [False, 100], to=current_user.username)
    
    """curr_room = current_user.username + "_room"
    curr_name = data.split("_room")[0]
    players = active_rooms[data].split(",")
    index = 0
    socketio.emit("show_table_cards", poker_games[curr_name].table_cards, to=data)
        
    for single_player in players:
        if single_player != "":
            print(single_player, flush=True)
            print(rooms())
            print("\n\n\n", flush=True)
            print(poker_games[curr_name].players[index].hand, flush=True)
            socketio.emit("show_cards",  poker_games[curr_name].players[index].hand, to=single_player)
            
            if index == 0: # give the turn to the first player
                socketio.emit("give_turn",  [True, 100], to=single_player)
            else:
                socketio.emit("give_turn",  [False, 100], to=single_player)
            index += 1"""
        

@socketio.on("bet")
def on_bet(data):
    if bool(data["turn"]) == True:
        poker_games[data["room"].split("_room")[0]].place_bet(20)
        current_player_index = active_rooms[data["room"]].split(",").index(current_user.username)
        number_of_players = len(active_rooms[data["room"]].split(",")) - 1
        
        list_of_players = active_rooms[data["room"]].split(",")
        list_of_players.pop() # eliminate the last player beacuse its void
        
        next_player_index = (current_player_index + 1)%number_of_players
        next_player = list_of_players[next_player_index]
        
        socketio.emit("give_turn", False, to=current_user.username)
        socketio.emit("give_turn", True, to=next_player)
        
        
        """if poker_games[data["room"].split("_room")[0]].turn_counter:
            poker_games[data["room"].split("_room")[0]].han"""
        
        #socketio.emit("give_starting_turn",  [False, 100], to=current_user.username)
        #socketio.emit("give_starting_turn",  [True, 100], to=next_player)
        
@socketio.on("leave_game")
def on_leave_game(data):
    if data["turn"] == True:
        pass



# route per la home page e la pagina "About"
@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html", title="Home Page")

@app.route("/info/")
def about():
    return render_template("info.html", title="Info Page")

# route per la pagina di login
@app.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate):
            login_user(user, remember=form.remember_me.data)
            flash('Benvenuto', category='success')
            return redirect('/home/')
        else:
            flash('Email o password sbagliate', category='danger')
            return redirect('/login/')
    else:
        return render_template("login.html", title="Login Page", form=form)


# route per la pagina di registrazione
@app.route("/register/", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data,
                    password=pw_hash,
                    email=form.email.data)
        with app.app_context():

            db.session.add(user)
            db.session.commit()

        flash(
            f"Il tuo account e' stato creato {form.username.data}", category="success")
        return redirect('/login/')

    return render_template("register.html", title="Pagina di Registrazione", form=form)
# route per la pagina dell'account
@app.route("/account/")
@login_required
def account():
    return render_template("account.html", title="Pagina dell'Account", p_bucks=current_user.p_bucks)

# route per la pagina dell'account
@app.route("/logout/")
@login_required
def log_out_user():
    logout_user()
    return render_template("home.html", title="Home Page")


# route per la pagina game
@app.route("/game/")
@login_required
def coming_soon():
    return render_template("room_selection.html", title="Coming Soon!", username=current_user.username)


# route per la pagina game
@app.route("/game_page/")
@login_required
def page_game():
    return render_template("game_page.html", title="game", username=current_user.username)
