from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('gr/<str:group_name>/', consumers.GroupConsumer.as_asgi()),
    path('ch/<int:chat_name>/', consumers.ChatConsumer.as_asgi()),
    path('rg/', consumers.RegistrationConsumer.as_asgi())
]