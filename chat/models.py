from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    last_message = models.IntegerField(default=0)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ('date_added',)