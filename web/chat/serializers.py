from django.utils.translation import gettext as _
from rest_framework import serializers

from main.services import MainService
from .services import ChatService


class CreateChatSessionSerializer(serializers.Serializer):
    room_id = serializers.UUIDField()
    asker_id = serializers.IntegerField(min_value=0)
    expert_id = serializers.IntegerField(min_value=0)
    message = serializers.CharField()

    def validate_room_id(self, room_id: int):
        if ChatService.is_room_exists(room_id):
            raise serializers.ValidationError(_("Room already exists"))
        return room_id

    def validate_asker_id(self, asker_id: int):
        if not MainService.is_user_client_exist(asker_id):
            raise serializers.ValidationError('Invalid id')
        return asker_id

    def validate_expert_id(self, expert_id: int):
        if not MainService.is_user_client_exist(expert_id):
            raise serializers.ValidationError('Invalid id')
        return expert_id

    def save(self):
        room = ChatService.create_users_room(**self.validated_data)
        return room.room_id
