import uuid
import base64
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from .managers import MessageManager, UsersRoomGroupManager
from main.models import UserClient


User = get_user_model()
FILE_TYPES = (
    ('img', 'image'),
    ('sound', 'sound'),
    ('file', 'file'),
)
IMG_FORMATS = ['jpg', 'jpeg', 'png', 'svg']
SOUND_FORMATS = ['wav', 'mp3']


def to_base64(text: str):
    e = base64.b64encode(text.encode("UTF-8"))
    return e.decode("UTF-8")


class Message(models.Model):
    author = models.ForeignKey(UserClient, related_name='message_set', on_delete=models.CASCADE)
    room_group = models.ForeignKey('RoomGroup', on_delete=models.CASCADE, null=True, default=None, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    received_at = models.DateTimeField(blank=True, null=True, db_index=True)
    is_system = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    objects = MessageManager()

    def __str__(self):
        return f"Message {self.author.id}"

    def clean(self):
        self.validate_user_group()

    def validate_user_group(self):
        if self.room_group not in get_user_rooms(self.author):
            raise ValidationError(f"User {self.author} does not have access to this room")

    def get_room_id(self):
        return str(self.room_group.room_id)
    get_room_id.short_description = 'Room id'

    def get_message_content_type(self):
        if self.message_file:
            return self.message_file.content_type
        return 'message'
    get_message_content_type.short_description = 'Content Type'

    class Meta:
        ordering = ('-created_at', '-received_at')


class UploadedFile(models.Model):
    filename = models.CharField(max_length=254, blank=True)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='message_file', null=True)
    url = models.URLField(max_length=400)
    content_type = models.CharField(choices=FILE_TYPES, max_length=100)
    file_id = models.PositiveIntegerField('File id in Customer Host')

    def save(self, **kwargs):
        self.content_type = self.get_file_format(self.url)
        self.filename = self.get_filename(self.url)
        self.url = to_base64(to_base64(self.url))
        return super().save(**kwargs)

    def get_file_format(self, url: str):
        file_format = url.rsplit('.', 1)[1]
        if file_format in IMG_FORMATS:
            return FILE_TYPES[0][0]
        elif file_format in SOUND_FORMATS:
            return FILE_TYPES[1][0]
        return FILE_TYPES[2][0]

    def get_filename(self, url: str):
        return url.rsplit('/', 1)[1]

    def __str__(self):
        return self.content_type


class RoomGroup(models.Model):
    room_id = models.UUIDField(null=False, editable=False, unique=True, default=uuid.uuid4)
    status = models.BooleanField('Open or close', default=1)  # default room is open
    objects = models.Manager()

    def __str__(self):
        return str(self.room_id)

    def add_users(self, users: list):
        UsersRoomGroup.objects.add_users_to_group(self, users)

    def room_users_id(self):
        return self.user_room_set.select_related('user').only('user__user_id').values_list('user__user_id', flat=True)


class UsersRoomGroup(models.Model):
    class Meta:
        unique_together = ('user', 'room_group')

    user = models.ForeignKey(UserClient, on_delete=models.CASCADE, related_name='user_room_set')
    room_group = models.ForeignKey(RoomGroup, on_delete=models.CASCADE, related_name='user_room_set')

    objects = UsersRoomGroupManager()

    def __str__(self):
        return '%s %s' % (self.user, self.room_group)


def get_user_rooms(user):
    user_group = UsersRoomGroup.objects.filter(user=user).values_list('room_group', flat=True).distinct()
    return RoomGroup.objects.filter(id__in=user_group).distinct()
