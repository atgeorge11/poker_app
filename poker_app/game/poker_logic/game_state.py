"""Class that holds general information about the game"""

import random
from .deck import deck

class Game_State():
    def __init__(self):

        #linked list containing data about players
        self.players = []
        
        #controls whether game has started or whether more players can joing
        self.playing = False

        #game state data
        self.dealer = None
        self.turn = None
        self.hands = {}
        self.used_cards = []
        self.better = None

    """generate a new player"""
    def generate_player(self, username, starting_chips, user_type):
        print("username", username)
        print("starting_chips", starting_chips)
        print("user_type", user_type)
        new_player =  {
            'player': username,
            'id': len(self.players),
            'chips': starting_chips,
            'user_type': user_type,
            'next': None,
            'status': "in",
            'bet': 0
        }

        #Insert player into linked list
        if new_player['id'] > 0:
            self.players[-1]['next'] = new_player['id']
        new_player['next'] = 0
        self.players.append(new_player)

    """remove a player from the game"""
    def remove_player(self, username):
        for idx, player in enumerate(self.players):
            if player['player'] == username:
                #Reattach other nodes of linked list before removing
                if len(self.players) > 1:
                    self.players[idx - 1]['next'] = player['next']
                self.players.remove(player) 
                break

    """returns the next player in the linked list"""
    def get_next_player(self, player):
        return self.players[player['next']]

    """starts the game"""
    def start_game(self):

        self.playing = True

        #Assign a dealer and deal
        self.dealer = random.randint(0, len(self.players) - 1)
        self.deal()

    """Method to draw a card"""
    def draw_card(self):
        idx = random.randint(0, 51)
        while id in self.used_cards:
            idx = random.randint(0, 51)
        self.used_cards.append(idx)
        return deck[idx]

    """Method to deal a hand"""
    def deal(self):
        #Start with player to the left of the dealer
        current_player = self.get_next_player(self.players[self.dealer])
        while current_player['id'] != self.dealer:
            if current_player['status'] != "out":
                self.hands[str(current_player['id'])] = [self.draw_card(), self.draw_card()]
            current_player = self.get_next_player(current_player)
        #Also deal to the dealer
        self.hands[str(current_player['id'])] = [self.draw_card(), self.draw_card()]

