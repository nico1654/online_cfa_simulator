class Player():
    def __init__(self):
        self.hand = list() 
        self.current_money = 100
        self.has_changed_hand = False
        self.has_betted_once = False
        self.has_leaved = False
        
    def first_bet(self, money_to_bet):
        if money_to_bet < self.current_money:
            self.current_money -= money_to_bet
        else:
            self.current_money -= 1
            return 1
        
        return money_to_bet
    
    #TODO elimino solo carte selezionate
    def change_card(self, cards_to_remove):
        if not self.has_changed_hand:
            for card in cards_to_remove:
                if card in self.hand:
                    self.hand.pop(self.hand.index(card))
            self.has_changed_hand = True
            
    
    def leave(self):
        self.hand = list()
        self.has_leaved = True

    def raise_bet(self, money_to_raise):
        if money_to_raise < self.current_money:
            self.current_money -= money_to_raise
        else:
            self.current_money -= 1
            return 1
        
        return money_to_raise
        
    