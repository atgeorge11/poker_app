#Class with methods to process messages from client websockets

from .poker_logic.hand_controller import Hand_Controller

class Message_Processor():
    def __init__(self, game_state):
        self.game_state = game_state
        self.broadcast = None

    def set_broadcast(self, broadcast):
        self.broadcast = broadcast

        #Create a method to generalize transmission of game state info to clients
        def broadcast_game_state(message_type, current_player=-1, listening=False):
            broadcast({
                'type': message_type,
                'state': {
                    'playing': True,
                    'dealer': self.game_state.dealer.id,
                    'players': self.process_players(),
                    'playersWithCards': self.get_players_with_cards(),
                    'currentPlayer': current_player,
                    'table': self.game_state.hand_controller.table,
                    'pot': self.game_state.hand_controller.pot,
                    'blind': self.game_state.blind,
                    'listening': listening,
                }
            })

        self.broadcast_game_state = broadcast_game_state

    def process_message (self, message, username, user_type):
        print(message['type'])
        if message['type'] == 'user_type_request':
            self.process_user_type_request (user_type)
        elif message['type'] == 'start_game':
            self.process_start_game ()
        elif message['type'] == 'call':
            self.process_call ()
        elif message['type'] == 'bet':
            self.process_bet (message['bet'])
        elif message['type'] == 'fold':
            self.process_fold ()

    def process_user_type_request (self, user_type):
        self.broadcast({
            'type': 'user_type_response',
            'user_type': user_type,
            'id': self.game_state.players[-1].id,
            'players': self.process_players()
        })

    def process_start_game (self):
        self.game_state.start_game()
    
    def process_call (self):
        self.game_state.hand_controller.handle_bet(-1)

    def process_bet (self, bet):
        self.game_state.hand_controller.handle_bet(bet)

    def process_fold (self):
        self.game_state.hand_controller.handle_fold()

    def process_players (self):
        output = []
        for player in self.game_state.players:
            output.append({
                'player': player.username,
                'id': player.id,
                'chips': player.chips,
                'user_type': player.user_type,
                'next': player.get_next().id,
                'prev': player.get_prev().id,
                'status': player.status,
                'bet': player.bet
            })
        return output

    """Returns an object that tracks the players who currently have cards"""
    def get_players_with_cards (self):
        output = {}
        for id in self.game_state.hand_controller.hands:
            output[id] = True
        return output

    def start_hand (self):
        pass
