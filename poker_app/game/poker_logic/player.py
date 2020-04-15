"""Class to represent a player"""

class Player():
    def __init__(self, username, starting_chips, user_type, id):
        self.username = username
        self.id = id
        self.chips = starting_chips
        self.user_type = user_type
        self.next = None
        self.prev = None
        self.status = 'in'
        self.bet = 0

    """return the next player"""
    def get_next(self):
        return self.next
    
    """set the next player"""
    def set_next(self, next_player):
        self.next = next_player

    """return the previous player"""
    def get_prev(self):
        return self.prev

    """set the previous player"""
    def set_prev(self, prev_player):
        self.prev = prev_player

    """make a bet"""
    def place_bet(self, amt):
        self.chips -= amt
        self.bet += amt
    
    
