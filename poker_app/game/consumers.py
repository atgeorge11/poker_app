import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = 'game_%s' % self.game_name

        #Join game group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        #Leave game group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    #Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'message',
                'message': data_json
            }
        )

    #Receive message from room group
    def message(self, event):
        message = event['message']

        #Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))