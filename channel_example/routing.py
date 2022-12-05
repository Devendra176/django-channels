from django.urls import re_path
from example import consumers


channel_routing = [
    re_path(r'^users/', consumers.UserConsumer.as_asgi()),
]
