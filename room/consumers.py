import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import User

from room.models import Room, Message


# class ChatConsumer(WebsocketConsumer):
#     """Синхронный вариант"""
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         self.send(text_data=json.dumps({"message": message}))


class ChatConsumer(AsyncWebsocketConsumer):
    """Асинхронный вариант"""

    async def connect(self):
        print("connect")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, *args):
        print("disconnect")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("receive")

        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        # Saving received massage
        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print("chat_message")

        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, room, message):
        print("save_message")

        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)


"""для инфо, что в scope"""
scope = {'type': 'websocket',
         'path': '/ws/first-room/',
         'raw_path': b'/ws/first-room/',
         'headers': [
             (b'host', b'127.0.0.1:8000'),
             (b'connection', b'Upgrade'),
             (b'pragma', b'no-cache'),
             (b'cache-control', b'no-cache'),
             (b'user-agent',
              b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'),
             (b'upgrade', b'websocket'),
             (b'origin', b'http://127.0.0.1:8000'),
             (b'sec-websocket-version', b'13'),
             (b'accept-encoding', b'gzip, deflate, br'),
             (b'accept-language', b'ru,ru-RU;q=0.9,en;q=0.8'),
             (b'cookie',
              b'csrftoken=He0A6l4uiotXCqaT9N2b6MNV4AJW2EbzjE3WFHcU2IfxrFou64u46A8ntd4kiyQt; sessionid=8ip1vr62tmvf64dffdtwhrrzwucb0cix'),
             (b'sec-websocket-key', b'2rJMgqYf0DWLev4XhxOAcA=='),
             (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits'),
         ],
         'query_string': b'',
         'client': ['127.0.0.1', 51664],
         'server': ['127.0.0.1', 8000],
         'subprotocols': [],
         'asgi': {'version': '3.0'},
         'cookies': {'csrftoken': 'He0A6l4uiotXCqaT9N2b6MNV4AJW2EbzjE3WFHcU2IfxrFou64u46A8ntd4kiyQt',
                     'sessionid': '8ip1vr62tmvf64dffdtwhrrzwucb0cix'},
         'session': '<django.utils.functional.LazyObject object at 0x000001CC5F96C0D0>',
         'user': '<channels.auth.UserLazyObject object at 0x000001CC5F96C790>',
         'path_remaining': '',
         'url_route': {'args': (), 'kwargs': {'room_name': 'first-room'}}}
