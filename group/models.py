from django.contrib.auth.models import User
from django.db import models
from main.models import Avatars

class Group(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)

class Message(models.Model):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)