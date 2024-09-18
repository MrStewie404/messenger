from django.urls import path

from .views import chats, chat, chat_search, create_chat

urlpatterns=[
    path('', chats, name='chats'),
    path('search/', chat_search, name='chat_search'),
    path('<slug:id>/', chat, name='chat'),
    path('<slug:id>/send/', create_chat, name='create_chat')
]