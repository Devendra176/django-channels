import  json

from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from example.models import LoggedInUser


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "users",
        {
            "type": "update_user",
            "value": json.dumps(
                    {
                        'username': kwargs.get('user').username,
                        'is_logged_in': True,
                    }
                )
        }
    )


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "users",
        {
            "type": "update_user",
            "value": json.dumps(
                    {
                        'username': kwargs.get('user').username,
                        'is_logged_in': False,
                    }
                )
        }
    )
