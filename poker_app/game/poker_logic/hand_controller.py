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
        self.side_pots = {}
        self.hands = {}

        self.message_processor = game_state.message_processor

    """play the small blind"""
    def small_blind(self):
        self.current_player.place_bet(math.ceil(self.blind / 2))
        self.emit_response(False, False)
        time.sleep(1)

        self.next_player()
        self.emit_response(False, False)
        time.sleep(1)

        self.next()

    """play the big blind"""
    def big_blind(self):
        self.current_player.place_bet(self.blind)
        self.emit_response(False, False)
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
            self.emit_response(False, False)
            time.sleep(1)
            self.next_player()
        self.next_player()
        self.next_player()
        self.emit_response(True, False)

    """handle a player's bet"""
    def handle_bet(self, amt):
        amt = int(amt)
        perform_end_check = True
        if amt > self.current_bet - self.current_player.bet: #if the player raised
            self.current_last_better = self.current_player
            perform_end_check = False
            self.current_bet = self.current_player.bet + amt
        self.current_player.place_bet(amt)
        self.emit_response(False, False)
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
        self.emit_response(False, False)
        time.sleep(1)

        #Check if there is only one player left
        in_players = []
        for player in self.count_in_players():
            in_players.append((player.id, 1000))
        if len(in_players) == 1:
            self.collect_bets()
            self.end_hand(in_players)
        else:
            self.handle_player_transition(perform_end_check)

    """handle transitions between players in a round of betting"""
    def handle_player_transition(self, perform_end_check):
        has_moved_once = False
        while has_moved_once == False or self.current_player.status == 'all_in':
            has_moved_once = True
            self.next_player()
            if perform_end_check == True and self.current_player is self.current_last_better:
                self.current_player = None
                self.collect_bets()
                self.current_bet = 0
                self.emit_response(False, False)
                self.next()
            else:
                self.emit_response(True, False)

    """Collects bets and deposit them in the pot"""
    def collect_bets(self):
        bets = []
        for player in self.game_state.players:
            if player.bet > 0:
                bets.append((player.id, player.bet))
        
        def player_sort_key (player_tuple):
            return player_tuple[1]

        bets.sort(key=player_sort_key)

        #collect any side pots
        for player in self.game_state.players:
            if player.status == 'all_in' and player.bet > 0:
                my_bet = 0
                bet_sum = 0
                for player_tuple in bets:
                    if my_bet == 0:
                        bet_sum += player_tuple[1]
                    else:
                        bet_sum += my_bet
                    if player_tuple[0] == player.id:
                        my_bet = player_tuple[1]
                self.side_pots[player.id] = self.pot + bet_sum

        #collect the main pots
        for player in self.game_state.players:
            self.pot += player.bet
            player.bet = 0

    """returns a list of players still in the hand"""
    def count_in_players(self):
        in_players = []
        for player in self.game_state.players:
            if player.status == 'in' or player.status =='all_in':
                in_players.append(player)
        return in_players

    """returns a list of players still in the game"""
    def count_playing_players(self):
        in_players = []
        for player in self.game_state.players:
            if player.status == 'in' or player.status =='all_in' or player.status == 'fold':
                in_players.append(player)
        return in_players

    """play the flop"""
    def flop(self):
        time.sleep(1)
        for num in range(3):
            self.table.append(self.deck.flip_card())
            self.emit_response(False, False)
            time.sleep(1)
        self.set_first_better()
        self.emit_response(True, False)

    """play the river or the turn"""
    def river_or_turn(self):
        time.sleep(1)
        self.table.append(self.deck.flip_card())
        self.emit_response(False, False)
        time.sleep(1)
        self.set_first_better()
        self.emit_response(True, False)

    """Score the hand and end the hand"""
    def score_hand(self):
        self.current_player = None
        self.emit_response(False, False)
        time.sleep(1)
        scores = Validator.validate(self.hands, self.table)

        int_scores = list(map(lambda x: (x[0], int(x[1], 16)), scores.items()))
        int_scores.sort(key=lambda x: x[1], reverse=True)

        self.end_hand(int_scores)
        
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
    def emit_response(self, listening, show_cards):
        current_player_id = -1
        if self.current_player is not None:
            current_player_id = self.current_player.id
        self.message_processor.broadcast_game_state('play', current_player_id, listening, show_cards)

    """Set the correct first better"""
    def set_first_better(self):
        self.current_player = self.game_state.dealer
        self.next_player()
        self.current_last_better = self.current_player

    """move to the next player still in the hand"""
    def next_player(self):
        self.current_player = self.game_state.get_next_in_player(self.current_player)

    """handle a player leaving the game"""
    def handle_player_leaving(self, player_id):
        print('handling player leaving')
        print(player_id, self.current_player)
        if self.current_player is not None and player_id == self.current_player.id:
            print('handling player transition')
            self.handle_player_transition(True)

    """end the hand"""
    def end_hand(self, sorted_players):

        time.sleep(1)

        self.emit_response(False, True)

        time.sleep(5)

        #create a list of all side pots from smallest to largest
        sorted_pots = list(map(lambda x: (x[0], x[1]), self.side_pots.items()))
        sorted_pots.sort(key=lambda x: x[1])

        #add the main pot to it for each remaining player
        print(self.side_pots)
        for player in sorted_players:
            print(player)
            if int(player[0]) not in self.side_pots:
                sorted_pots.append((int(player[0]), self.pot))

        print(sorted_pots)

        #amass the current winners
        winners = []
        high_score = sorted_players[0][1]
        tracker = 0

        while tracker < len(sorted_players) and sorted_players[tracker][1] == high_score:
            winners.append(int(sorted_players[tracker][0]))
            tracker += 1

        num_winners = len(winners)

        #allot each pot from smallest to largest
        for pot in sorted_pots:
            #if the owner of the pot is a winner
            if self.pot > 0 and pot[0] in winners:
                winnings = min(pot[1], self.pot) / num_winners
                self.game_state.players[pot[0]].chips += winnings
                self.pot -= winnings
                #remove player from winners
                winners.remove(pot[0])
                #get next set of winners if there are none left
                if len(winners) == 0 and tracker < len(sorted_players):
                    high_score = sorted_players[tracker][1]
                    while tracker < len(sorted_players) and sorted_players[tracker][1] == high_score:
                        winners.append(int(sorted_players[tracker][0]))
                        tracker += 1
                    num_winners = len(winners)

        #remove players with no chips from the game
        for player in self.game_state.players:
            if player.chips == 0:
                player.status = 'out'

        #self.pot = 0
        self.emit_response(False, False)
        time.sleep(2)

        #start the next hand or end the game depending on number of remaining players
        in_players = self.count_playing_players()
        if len(in_players) > 1:
            self.game_state.start_hand()
        else:
            print('ending game')
            self.message_processor.broadcast_end_game(in_players[0].id)