import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.utils import timezone

from chat.services import AsyncChatService
from main.models import UserClient


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class AsyncChatConsumer(AsyncJsonWebsocketConsumer):
    async def message_content(self, **kwargs) -> dict:
        content = {
            'author': {
                'id': kwargs.get('author') or self.user.user_id
            },
            'id': kwargs.get('id', ''),
            'type': kwargs.get('type', 'message'),
            'message': kwargs.get('message', ''),
            'created_at': kwargs.get('created_at', str(timezone.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'))),
            'is_system': kwargs.get('is_system', False)
        }
        return content

    async def connect(self):
        self.user = self.scope.get('user')
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        await self.initial_validate()
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()
        await self.system_chat_message(
            await self.message_content(type='system', message='connected')
        )

    async def initial_validate(self):
        if not isinstance(self.user, UserClient):
            await self.close()
        if not await AsyncChatService.is_room_open(self.room_id):
            await self.close()
        if not await AsyncChatService.is_user_in_room(self.room_id, self.user):
            await self.close()
        self.room = await AsyncChatService.get_group_by_id(room_id=self.room_id)
        if not self.room:
            await self.close()

    async def system_chat_message(self, data):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'system.message',
                'data': data
            }
        )

    async def system_message(self, data: dict):
        await self.send_message(message=data.get('data'))

    async def send_message(self, message):
        await self.send_json(content=message)

    async def new_message(self, data):
        message = data.get('message')
        message_obj = await AsyncChatService.save_chat_message(message=message, user=self.user, room=self.room)
        data['id'] = message_obj.id
        data['author'] = data.get('author')
        data['created_at'] = str(message_obj.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'chat.message',
                'data': data
            }
        )

    async def chat_message(self, event: dict):
        content = await self.message_content(
            id=event['data']['id'],
            author=event['data']['author'],
            message=event['data']['message'],
            created_at=event['data']['created_at'],
        )
        await self.send_message(message=content)

    async def write_message(self, data: dict):
        message = await self.message_content(
            author=data.get('author'),
            type='system',
            message=data['message'],
        )

        await self.system_chat_message(message)

    commands = {
        'new_message': new_message,
        'write_message': write_message
    }

    async def receive_json(self, content, **kwargs):
        await self.commands[content['command']](self, content)

    async def disconnect(self, close_code):
        await self.system_chat_message(
            await self.message_content(type='system', message='disconnected')
        )
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
