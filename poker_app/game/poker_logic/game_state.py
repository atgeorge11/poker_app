"""Class that holds general information about the game"""

import random
from .player import Player
from ..message_processor import Message_Processor
from .hand_controller import Hand_Controller

class Game_State():
    def __init__(self):

        #Create a message processor
        self.message_processor = Message_Processor(self)

        #linked list containing data about players
        self.players = []
        
        #controls whether game has started or whether more players can join
        self.playing = False

        #game state data
        self.dealer = None
        self.blind = 10

        #information about the current hand
        self.hand_controller = None

    """generate a new player"""
    def generate_player(self, username, starting_chips, user_type):

        new_player = Player(username, starting_chips, user_type, len(self.players))

        #Insert player into linked list
        if new_player.id == 0:
            new_player.set_next(new_player)
            new_player.set_prev(new_player)
        else:
            new_player.set_next(self.players[0])
            new_player.set_prev(new_player.get_next().get_prev())
            new_player.get_next().set_prev(new_player)
            new_player.get_prev().set_next(new_player)

        #Add player to players list
        self.players.append(new_player)

    """remove a player from the game"""
    def remove_player(self, player):
        #Set player's status to 'out'
        player.status = 'out'
        player.chips = 0

        print('made it to remove_player')

        if self.hand_controller is not None:
            print('hand controller is operating')
            self.hand_controller.hands[str(player.id)] = []
            self.hand_controller.handle_player_leaving(player.id)

        """
        #Reconnect other noes of linked list before deleting
        if len(self.players) > 1:
            player.get_prev().set_next(player.get_next())
            player.get_next().set_prev(player.get_prev())

        #Reassign player's idx in players list
        #Do not delete the idx; we need to retain the spot for index accessing
        self.players[player.id] = None

        #Delete the player
        del player
        """

    """returns the next player still in the hand"""
    def get_next_in_player(self, player):
        next_player = player.get_next()
        while(next_player.status != 'in' and next_player.status != 'all_in'):
            next_player = next_player.get_next()
        return next_player

    """starts the game"""
    def start_game(self):

        self.playing = True

        #Assign a dealer and start hand
        self.dealer = self.get_random_player()
        self.start_hand()

    """returns a random player"""
    def get_random_player(self):
        rand_num = random.randint(0, 19)
        player = self.players[0]
        for iter in range(0, rand_num):
            player = player.get_next()
        return player

    """starts a hand"""
    def start_hand(self):
        #Reset every player's status to in
        for player in self.players:
            if player.status != 'out':
                player.status = 'in'
        self.dealer = self.get_next_in_player(self.dealer)
        self.hand_controller = Hand_Controller(self)
        self.hand_controller.next()