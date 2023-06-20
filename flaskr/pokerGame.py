import random
from flaskr.Deck import Deck
from flaskr.Player import Player


class PokerGame:
    def __init__(self, number_of_players):
        self.deck = Deck()
        self.pot = 0
        self.players = list()
        for single_player in range(number_of_players):
            self.players.append(Player())
        self.table_cards = list()
        self.current_bet = 0
        self.minimum_bet = 10
        self.active_players = []
        self.inactive_players = []
        self.current_player = None
        self.round_count = 0
        self.turn_counter = 0
        
    def start_game(self):
        self.put_table_card()
        self.deal_cards()
        
        self.current_player = self.players[0]
        self.active_players = self.players.copy()
        self.inactive_players = []
        self.round_count = 0
        #self.ask_players_for_action()

    def deal_cards(self):
        #for player in self.players:
        for index in range(len(self.players)):
            self.players[index].hand = [self.deck.pick_cards(5)]
            print(self.players[index].hand, flush=True)

    def put_table_card(self):
        self.table_cards = self.deck.pick_cards(5)

    def place_bet(self, bet):
        self.pot += bet
        self.turn_counter += 1
    
    def place_small_blind(self):
        small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        small_blind_player.bet(self.minimum_bet // 2)
        self.pot += small_blind_player.bet_amount

    def place_big_blind(self):
        big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]
        big_blind_player.bet(self.minimum_bet)
        self.pot += big_blind_player.bet_amount

    def ask_players_for_action(self):
        self.round_count += 1
        if self.round_count == 1:
            self.burn_card()
            self.flop()
        elif self.round_count == 2:
            self.burn_card()
            self.turn()
        elif self.round_count == 3:
            self.burn_card()
            self.river()
        else:
            self.end_game()
            return
        
        for player in self.active_players:
            if player == self.current_player:
                continue
            player.on_player_turn()
            
        action = self.current_player.on_player_turn()
        if action == 'fold':
            self.player_fold()
        elif action == 'call':
            self.player_call()
        elif action == 'raise':
            self.player_raise()
        else:
            self.ask_players_for_action()

    def burn_card(self):
        self.deck.draw_card()
        
    def check_winner(self):
        card_count = {"D": 0, "S": 0, "H":0, "C":0}
        for card in self.table_cards:
            card_count[card[len(card) - 1]] += 1
        
        
        winner_symbol = max(card_count, key=card_count.get)
        print(winner_symbol, flush=True)
        print("\n\n\n", flush=True)
        
        player_cards = [{"D": 0, "S": 0, "H":0, "C":0} for i in range(len(self.players))]
        print(player_cards, flush=True)
        player_symbol = []
        player_index = 0
        for single_player in self.players:
            for card in single_player.hand:
                player_symbol = card[len(card) - 1]
                player_cards[player_index][player_symbol] += 1
            player_symbol.append(max(player_cards[player_index], key=player_cards[player_index].get))
            player_index += 1
        
        print(player_symbol, flush=True)
    
        