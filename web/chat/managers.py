from django.db import models

from main.services import MainService


class MessageManager(models.Manager):
    def get_messages_by_group(self, room_group):
        return self.filter(room_group=room_group).order_by('-created_at')

    def get_unread_messages_by_group(self, user, room_group):
        return self.filter(room_group=room_group, received_at=None)\
            .exclude(author=user).order_by('-created_at')


class UsersRoomGroupManager(models.Manager):

    def add_users_to_group(self, room_group, users: list):
        for user_id in users:
            user = MainService.get_user_client(user_id)
            self.create(user=user, room_group=room_group)

    def delete_users_from_group(self, room_group, users):
        for user in users:
            self.filter(user=user, room_group=room_group).delete()
