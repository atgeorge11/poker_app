import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .poker_logic.game_states import game_states
from .message_processor import process_message

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = 'game_%s' % self.game_name
        self.username = self.scope['user'].username

        #Deny connection if game doesn't exist or is already in play
        if self.game_name not in game_states or game_states[self.game_name].playing == True:
            return

        #save reference to game_state
        self.game_state = game_states[self.game_name]

        #Determine whether player is host by checking current number of players
        if len(self.game_state.players) == 0:
            self.user_type = 'host'
        else:
            self.user_type = 'guest'

        #Add player to game model
        self.game_state.generate_player(self.username, 1000, self.user_type)

        #Join game group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        #if player is host, end the game
        if self.user_type == 'host':
            #end game
            pass        

        #Remove player from game model
        self.game_state.remove_player(self.username)

        print('player leaving', self.game_state.players)

        #Send message to remaining players
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'message',
                'message': {
                    'type': 'user_type_response',
                    'user_type': self.user_type,
                    'players': self.game_state.players
                }
            }
        )

        #Leave game group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    #Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)

        message = process_message(data_json, self.game_state, self.username, self.user_type)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'message',
                'message': message
            }
        )

    #Receive message from room group
    def message(self, event):
        message = event['message']

        #Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))