from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.models import User
from chat.models import Thread, Message

import json


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Inside connect")
        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = await sync_to_async(User.objects.get)(username=other_username)
        self.thread_obj = await sync_to_async(Thread.objects.get_or_create_personal_thread)(me, other_user)
        self.room_name = f'presonal_thread_{self.thread_obj.id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })
        print(f'[{self.channel_name}] - You are connected')

    async def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Recieved message - {event["text"]}')

        msg = json.dumps({
            'text': event.get('text'),
            'username': self.scope['user'].username
        })

        await self.store_message(event.get('text'))

        await self.channel_layer.group_send(
            self.room_name,
             {
                'type': 'websocket.message',
                'text': msg
             }
        )

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event["text"]}')
        await self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disonnected')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_message(self, text):
        Message.objects.create(
            thread = self.thread_obj,
            sender = self.scope['user'],
            text = text
        )


class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.room_name = 'broadcast'
        self.send({
            'type': 'websocket.accept'
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f'[{self.channel_name}] - You are connected')

    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Recieved message - {event["text"]}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
             {
                'type': 'websocket.message',
                'text': event.get('text')
             }
        )

    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disonnected')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)