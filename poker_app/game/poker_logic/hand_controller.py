"""A class to handle information about the current hand"""

import time, math
from .deck import Deck

class Hand_Controller():

    def __init__(self, game_state):
        self.game_state = game_state
        self.status = 'busy' #listening for user input?
        self.phase = -1
        self.current_player = game_state.get_next_in_player(game_state.dealer)
        self.blind = self.game_state.blind
        self.deck = Deck()
        self.table = []
        self.hands = {}

        self.message_processor = game_state.message_processor

    """play the small blind"""
    def small_blind(self):
        self.current_player.place_bet(math.ceil(self.blind / 2))
        self.emit_response()
        time.sleep(1)

        self.next_player()
        self.emit_response()
        time.sleep(1)

        self.next()

    """play the big blind"""
    def big_blind(self):
        self.current_player.place_bet(self.blind)
        self.emit_response()
        time.sleep(1)

        self.next()

    """deal the cards"""
    def deal(self):
        self.current_player = self.game_state.dealer
        while str(self.current_player.id) not in self.hands:
            self.hands[str(self.current_player.id)] = [
                self.deck.flip_card(),
                self.deck.flip_card()
            ]
            self.emit_response()
            time.sleep(1)
            self.next_player()

    """play the flop"""
    def flop(self):
        pass

    """play the river"""
    def river(self):
        pass

    """play the turn"""
    def turn(self):
        pass

    """run the next phase of the hand"""
    def next(self):
        phases = [
            self.small_blind,
            self.big_blind,
            self.deal,
            self.flop,
            self.river,
            self.turn
        ]

        self.phase += 1
        phases[self.phase]()

    """send the game state to the clients"""
    def emit_response(self):
        self.message_processor.broadcast_game_state('play', self.current_player.id)

    """move to the next player still in the hand"""
    def next_player(self):
        self.current_player = self.game_state.get_next_in_player(self.current_player)

