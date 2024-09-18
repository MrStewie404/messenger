from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('gr/<str:room_name>/', consumers.GroupConsumer.as_asgi()),
    path('ch/<int:room_name>/', consumers.ChatConsumer.as_asgi())
]