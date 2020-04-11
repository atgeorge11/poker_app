import json
from channels.generic.websocket  import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    def connect(self):
        print("accepting")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.send(text_data=json.dumps({
            'message': data_json
        }))