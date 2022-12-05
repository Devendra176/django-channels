import json

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

    def receive(self, text_data=None):
        if not json.loads(text_data).get('active'):
            async_to_sync(self.channel_layer.group_send)(
                    "users",
                    {
                        "type": "update_user",
                        "value": json.dumps(
                                {
                                    'username': self.user.username,
                                    'is_logged_in': False,
                                }
                            )
                    }
                )
        if json.loads(text_data).get('active'):
            async_to_sync(self.channel_layer.group_send)(
                "users",
                {
                    "type": "update_user",
                    "value": json.dumps(
                            {
                                'username': self.user.username,
                                'is_logged_in': True,
                            }
                        )
                }
            )

    def update_user(self, event):
        data = event.get('value')
        self.send(text_data=data)
