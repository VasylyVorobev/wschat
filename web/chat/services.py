from channels.db import database_sync_to_async
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from main.models import UserClient
from main.services import MainService
from .models import Message, RoomGroup, UsersRoomGroup


class AsyncChatService:
    @staticmethod
    @database_sync_to_async
    def get_group_by_id(room_id):
        try:
            return RoomGroup.objects.get(room_id=room_id)
        except RoomGroup.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def is_room_open(room_id: int):
        try:
            return RoomGroup.objects.get(room_id=room_id).status
        except RoomGroup.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def is_user_in_room(room_id, user):
        return UsersRoomGroup.objects.filter(Q(user=user) & Q(room_group__room_id=room_id)).exists()

    @staticmethod
    @database_sync_to_async
    def save_chat_message(message, user, room):
        return Message.objects.create(author=user, room_group=room, message=message)


class ChatService:
    @staticmethod
    def is_room_exists(room_id: int) -> bool:
        return RoomGroup.objects.filter(id=room_id).exists()

    @staticmethod
    def create_users_room(**data) -> RoomGroup:
        room = RoomGroup.objects.create(room_id=data.get('room_id'))
        room.add_users([data.get('asker_id'), data.get('expert_id')])
        return room

    @staticmethod
    def get_group_by_id(room_id: int):
        return get_object_or_404(RoomGroup, room_id=room_id)

    @staticmethod
    def socket_chat_created(data: dict) -> None:
        message = f"""<div><b>Question:</b>{data.get('message')}</div>"""
        author = MainService.get_user_client(data.get('asker_id'))
        room = ChatService.get_group_by_id(data.get('room_id'))
        ChatService.save_chat_message(user=author, message=message, room=room, is_system=True)

    @staticmethod
    def save_chat_message(message: str, user: UserClient, room: RoomGroup, is_system: bool) -> Message:
        return Message.objects.create(author=user, room_group=room, message=message, is_system=is_system)
