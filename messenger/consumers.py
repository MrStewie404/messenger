import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger.settings')
django.setup()

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from group.models import Message as GroupMessage, Group
from chat.models import Message as ChatMessage, Chat

class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, _):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        group = data['group']

        await self.save_message(username, group, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'group': group
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        group = event['group']

        avatar, user_id, first_name, last_name = await self.get_info(username)

        await self.send(text_data=json.dumps({
            'message': message,
            # 'username': username,
            'first_name': first_name,
            'last_name': last_name,  
            'group': group,
            'avatar_path': avatar,
            'user_id': user_id
        }))

    @sync_to_async
    def get_info(self, username):
        user = User.objects.get(username=username)
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        messages = GroupMessage.objects.filter(user=user)

        avatars = []
        for message in messages:
            user = message.user
            avatar = user.avatars.first()
            avatars.append(avatar)

        return str(avatars[0].path.url), user_id, first_name, last_name

    @sync_to_async
    def save_message(self, username, group, message):
        user = User.objects.get(username=username)
        group = Group.objects.get(slug=group)

        GroupMessage.objects.create(
            user=user, 
            group=group,
            text=message
        )



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, _):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['userID']
        chat_id = data['chat']

        await self.save_message(user_id, chat_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'userID': user_id,
                'chat': chat_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['userID']
        chat_id = event['chat']

        # avatar, user_id, username = await self.get_avatar(user_id)
        user_id, username = await self.get_avatar(user_id)

        await self.send(text_data=json.dumps({
            'message': message,
            # 'username': username,
            'chat_id': chat_id,
            # 'avatar_path': avatar,
            'user_id': user_id
        }))

    @sync_to_async
    def get_avatar(self, id):
        user = User.objects.get(id=id)
        user_id = user.id
        username = user.username
        # messages = ChatMessage.objects.filter(user=user)

        # avatars = []
        # for message in messages:
        #     user = message.sender
        #     avatar = user.avatars.first()
        #     avatars.append(avatar)

        # return str(avatars[0].path.url), user_id, username
        return user_id, username

    @sync_to_async
    def save_message(self, id, chat_id, message):
        sender = User.objects.get(id=id)

        ChatMessage.objects.create(
            sender=sender, 
            chat_id=chat_id,
            text=message
        )