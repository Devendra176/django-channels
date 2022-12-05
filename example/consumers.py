from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'users'
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, message):
        self.group_name = 'users'
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )
    
    def update_user(self, event):
        data = event.get('value')
        self.send(text_data=data)
