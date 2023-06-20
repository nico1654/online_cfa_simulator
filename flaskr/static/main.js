playing = true
$(document).ready(function(){
    
    $("#exit_room").hide();
    $("#start_game").hide();
    //$("give_cards").hide();
    /**
     * function create when the user open the game page
     * It creates the socket for the communication
     */
    var socket = io() 
    socket.on('connect', function() {
        console.log("connected")
        socket.emit("startInfo")
    });
    
    
    /**
     * after testing delete this
     */
    /*socket.on("color", function(msg) {
        if(msg == "red"){
            console.log("test_red")
            $("#containGame").css("background-color", "red")

        }else if(msg == "yellow"){
            console.log("test_yellow")
            $("#containGame").css("background-color", "yellow")
        }
    });*/


    /**
     * function called when we want to update the avaiable room
     */
    socket.on("load_avaiable_rooms", function(data) {
        $('#avaiableRooms').empty();
        Object.keys(data).forEach(key => {
            var room_button = $('<input type="button" value=' + key + '"/>')
            .attr('class', 'enter_room')
            .attr('id', key)
            .click(f => {
                socket.emit('enter_existing_room',{"room": key, "username":"username"});
                $('#avaiableRooms').hide();
            });
            room_button.appendTo($("#avaiableRooms"));
        });
    });

    /**
     * function called when a user enter the game page
     */
    socket.on("setup", function(data) {
        $('#avaiableRooms').empty();
        Object.keys(data).forEach(key => {
            var room_button = $('<input type="button" value=' + key + '"/>')
            .attr('class', 'enter_room')
            .attr('id', key)
            .click(f => {
                socket.emit('enter_existing_room', {"room": key, "username":"username"});
                $('#avaiableRooms').hide();
            });
            room_button.appendTo($("#avaiableRooms"));
        });
    });

    /**
     * function used to save the current room for the user
     */
    socket.on("send_current_room", function(data) {
        localStorage.setItem("current_room", data)
        $('#create_room').hide();
        $("#exit_room").show();
    });

    /**
     * when the first player start the game every user will generate the new page
     */
    socket.on("load_game_page", function(data) {
        $("body").load("/game_page/", function(){
            socket.emit("give_cards", localStorage.getItem("current_room"));   //emit the request to get the cards
        });
    });
    
    /**
     * when the card are getted i show them in the browser
     */
    socket.on("show_cards", function(data) {
        data[0].forEach(elem => {
            var symbol = "&clubs;"
            switch(elem[elem.length - 1]){
                case "C":
                    symbol = "&clubs;"
                    break
                case "H":
                    symbol = "&hearts;"
                    break
                case "S":
                    symbol = "&spades;"
                    break
                case "D":  
                    symbol = "&diams;"
                    break
                default:
                    symbol = "&hearts;" 
                    break 
            }
            number = elem.substring(0, elem.length-1)
            $("#player_hand").append("<div class='card-small'><p class='card-text black'>"+ number +"</p><p class='card-img black'>"+ symbol +"</p></div>")
        });
    });


    /**
     * when the table card are getted i show them in the browser
     */
    socket.on("show_table_cards", function(data) {
        data.forEach(elem => {
            var symbol = "&clubs;"
            console.log(elem[elem.length - 1])
            switch(elem[elem.length - 1]){
                case "C":
                    symbol = "&clubs;"
                    break
                case "H":
                    symbol = "&hearts;"
                    break
                case "S":
                    symbol = "&spades;"
                    break
                case "D":  
                    symbol = "&diams;"
                    break
                default:
                    symbol = "&hearts;" 
                    break 
            }
            number = elem.substring(0, elem.length-1)
            $(".board").append("<div class='card-small'><p class='card-text black'>"+ number +"</p><p class='card-img black'>"+ symbol +"</p></div>")
        });
    });



    /**
     * set the turn for each player after one of them do something
     */
    socket.on("give_turn", function(data) {
        console.log("il tuo turno è");
        console.log(data);
        localStorage.setItem("is_current_turn", data);
        console.log(typeof(localStorage.getItem("is_current_turn")));
        //localStorage.setItem("current_money", 100);
    });

    /**
     * set the starting turn for each player
     */
    socket.on("give_starting_turn", function(data) {
        console.log("dato primo turno")
        localStorage.setItem("is_current_turn", data[0]);
        localStorage.setItem("current_money", 100);
    });



    /*$('#start').click(function(){
        socket.emit("change_color", {"color":"red", "current_room": localStorage.getItem("current_room")}) 
    });

    $('#finish').click(function(){
        socket.emit("change_color", {"color":"yellow", "current_room": localStorage.getItem("current_room")}) 
    });*/
    
    /**
     * function called when we want to create a new room
     */
    $('#create_room').click(function(){
        socket.emit('join', {"room": "room", "username":"username"});
        $('#avaiableRooms').hide();
        $('#start_game').show();
    });

    /**
     * function called when the user want to exit the current room
     */
    $('#exit_room').click(function(){
        console.log("exit_room")
        socket.emit('leave_room', {"room": localStorage.getItem("current_room")}); 
        $('#create_room').show();
        $('#avaiableRooms').show();
        $("#exit_room").hide();
        $('#start_game').hide();
    });
    
    $("#start_game").click(function() {
        socket.emit("start_game", {"room": localStorage.getItem("current_room")})
    });


    $("#bet").click(function() {
        if(parseInt(localStorage.getItem("current_money")) >= 20 && localStorage.getItem("is_current_turn") == "true"){
            socket.emit("bet", {"room": localStorage.getItem("current_room"), 
        "turn": localStorage.getItem("is_current_turn"),
        "money": localStorage.getItem("current_money")});
        var new_money = (parseInt(localStorage.getItem("current_money")) - 20)
        localStorage.setItem("current_money", new_money)
        console.log(localStorage.getItem("current_money"))
        console.log(new_money)
        }else{
            alert("NON PUOI SCOMMETTERE");
        }
        
    });

    $("#leave").click(function() {
        socket.emit("leave_game", {"room": localStorage.getItem("current_room"), 
        "turn": localStorage.getItem("is_current_turn")});
    });




    /*function match_room(){
        socket.emit('join',{"room": "room", "username":"username"});
    };*/
})