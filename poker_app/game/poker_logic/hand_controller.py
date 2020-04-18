"""A class to handle information about the current hand"""

import time, math
from .deck import Deck
from .validator.validator import Validator

class Hand_Controller():

    def __init__(self, game_state):
        self.game_state = game_state
        self.status = 'busy' #listening for user input?
        self.phase = -1
        self.current_player = game_state.get_next_in_player(game_state.dealer)
        self.current_last_better = None
        self.current_bet = 0
        self.blind = self.game_state.blind
        self.deck = Deck()
        self.table = []
        self.pot = 0
        self.hands = {}

        self.message_processor = game_state.message_processor

    """play the small blind"""
    def small_blind(self):
        self.current_player.place_bet(math.ceil(self.blind / 2))
        self.emit_response(False)
        time.sleep(1)

        self.next_player()
        self.emit_response(False)
        time.sleep(1)

        self.next()

    """play the big blind"""
    def big_blind(self):
        self.current_player.place_bet(self.blind)
        self.emit_response(False)
        time.sleep(1)
        
        self.current_bet = self.blind
        self.current_last_better = self.game_state.get_next_in_player(self.current_player)
        self.next()

    """deal the cards"""
    def deal(self):
        self.current_player = self.game_state.dealer
        self.next_player()
        while str(self.current_player.id) not in self.hands:
            self.hands[str(self.current_player.id)] = [
                self.deck.flip_card(),
                self.deck.flip_card()
            ]
            self.emit_response(False)
            time.sleep(1)
            self.next_player()
        self.next_player()
        self.next_player()
        self.emit_response(True)

    """handle a player's bet"""
    def handle_bet(self, amt):
        amt = int(amt)
        perform_end_check = True
        bet = self.current_bet - self.current_player.bet
        if amt != -1: #if the player raised
            print("betting")
            self.current_last_better = self.current_player
            self.current_bet += amt
            perform_end_check = False
            bet += amt
        self.current_player.place_bet(bet)
        self.emit_response(False)
        time.sleep(1)
        self.handle_player_transition(perform_end_check)

    """handle a player's fold"""
    def handle_fold(self):
        perform_end_check = True
        #if current_last_better, move that designation to the next in player
        if self.current_player is self.current_last_better:
            self.current_last_better = self.game_state.get_next_in_player(self.current_player)
            perform_end_check = False

        self.hands[str(self.current_player.id)] = []
        self.current_player.status = "fold"
        self.pot += self.current_player.bet
        self.current_player.bet = 0
        self.emit_response(False)
        time.sleep(1)

        #Check if there is only one player left
        in_players = self.count_in_players()
        if len(in_players) == 1:
            self.end_hand(in_players[0])
        else:
            self.handle_player_transition(perform_end_check)

    """handle transitions between players in a round of betting"""
    def handle_player_transition(self, perform_end_check):
        self.next_player()
        if perform_end_check == True and self.current_player is self.current_last_better:
            print('hit end check')
            self.current_player = None
            self.collect_bets()
            self.current_bet = 0
            self.emit_response(False)
            self.next()
        else:
            print('passed end check')
            self.emit_response(True)

    """Collects bets and deposit them in the pot"""
    def collect_bets(self):
        for player in self.game_state.players:
            self.pot += player.bet
            player.bet = 0

    """returns a list of players still in the hand"""
    def count_in_players(self):
        in_players = []
        for player in self.game_state.players:
            if player.status == 'in':
                in_players.append(player)
        return in_players

    """play the flop"""
    def flop(self):
        time.sleep(1)
        for num in range(3):
            self.table.append(self.deck.flip_card())
            self.emit_response(False)
            time.sleep(1)
        self.set_first_better()
        self.emit_response(True)

    """play the river or the turn"""
    def river_or_turn(self):
        time.sleep(1)
        self.table.append(self.deck.flip_card())
        self.emit_response(False)
        time.sleep(1)
        self.set_first_better()
        self.emit_response(True)

    """Score the hand and return the scores to the client"""
    def score_hand(self):
        self.current_player = None
        self.emit_response(False)
        time.sleep(1)
        scores = Validator.validate(self.hands, self.table)
        print(scores)


    """run the next phase of the hand"""
    def next(self):
        phases = [
            self.small_blind,
            self.big_blind,
            self.deal,
            self.flop,
            self.river_or_turn,
            self.river_or_turn,
            self.score_hand
        ]

        self.phase += 1
        phases[self.phase]()

    """send the game state to the clients"""
    def emit_response(self, listening):
        current_player_id = -1
        if self.current_player is not None:
            current_player_id = self.current_player.id
        self.message_processor.broadcast_game_state('play', current_player_id, listening)

    """Set the correct first better"""
    def set_first_better(self):
        self.current_player = self.game_state.dealer
        if self.current_player.status != "in":
            self.next_player()

    """move to the next player still in the hand"""
    def next_player(self):
        self.current_player = self.game_state.get_next_in_player(self.current_player)

    """end the hand"""
    def end_hand(self, winner):
        self.collect_bets()
        winner.chips += self.pot
        self.pot = 0
        self.emit_response(False)
        time.sleep(1)
        self.game_state.start_hand()

