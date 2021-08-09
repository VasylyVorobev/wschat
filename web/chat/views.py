from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from . import serializers
from .services import ChatService


class CreateChatSessionView(GenericAPIView):
    serializer_class = serializers.CreateChatSessionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_id = serializer.save()
        data: dict = serializer.data
        data.update({'room_id': room_id})
        ChatService.socket_chat_created(data)


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
