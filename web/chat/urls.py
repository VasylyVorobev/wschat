from django.urls import path
from . import views


urlpatterns = [
    path('room/create/', views.CreateChatSessionView.as_view(), name='chat_create'),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
