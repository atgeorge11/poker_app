import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import threading

from .poker_logic.game_states import game_states

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = 'game_%s' % self.game_name
        self.username = self.scope['user'].username
        self.id = None
        self.user_type = None

        #Deny connection if game doesn't exist or is already in play
        if self.game_name not in game_states or game_states[self.game_name].playing == True:
            return

        #save reference to game_state and message_processor
        self.game_state = game_states[self.game_name]
        self.message_processor = self.game_state.message_processor

        #Join game group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        #Determine whether player is host by checking current number of players
        if len(self.game_state.players) == 0:
            self.user_type = 'host'
            #Also give message_processor access to broadcast
            self.message_processor.set_broadcast(self.produce_broadcast_function(self.channel_layer, self.game_group_name))
        else:
            self.user_type = 'guest'

        #Add player to game model
        self.game_state.generate_player(self.username, 1000, self.user_type)

        self.accept()

    def disconnect(self, close_code):
        #if player is host, end the game
        if self.user_type == 'host':
            #end game
            pass

        #Remove player from game model
        if self.game_state is not None:
            self.game_state.remove_player(self.game_state.players[self.id])

        print('player leaving', self.game_state.players)

        #Send message to remaining players
        self.broadcast({
            'type': 'message',
            'message': {
                'type': 'user_type_response',
                'user_type': self.user_type,
                'players': self.game_state.players
            }
        })

        #Leave game group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    #produce a function to send a message to group
    def produce_broadcast_function(self, channel_layer, game_group_name):
        def broadcast (message):
            async_to_sync(channel_layer.group_send)(
                game_group_name,
                    {
                        'type': 'message',
                        'message': message
                    }
                )
        return broadcast
    
    #Send a message to group
    def broadcast (self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'message',
                'message': message
            }
        )

    #Receive message from WebSocket; starts a new thread to run the game logic
    def receive(self, text_data):
        data_json = json.loads(text_data)
        thread = threading.Thread(
            target=self.message_processor.process_message,
            args=(data_json, self.username, self.user_type)
        )
        thread.start()

    #Receive message from group
    def message(self, event):
        message = event['message']

        #Grab id if user_type_request
        if self.id is None and message['type'] == "user_type_response":
            self.id = message['id']
        elif message['type'] == 'play':
            #Insert player's hand if possible
            if self.game_state.hand_controller is not None and str(self.id) in self.game_state.hand_controller.hands:
                message['state']['hand'] = self.game_state.hand_controller.hands[str(self.id)]
            else:
                message['state']['hand'] = None

        #Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))