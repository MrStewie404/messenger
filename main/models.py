from django.db import models
from django.contrib.auth.models import User

class Avatars(models.Model):
    path = models.ImageField(upload_to='static/media/avatars/', 
                             default='static/media/avatars/default.jpg')
    user = models.ForeignKey(User, related_name='avatars', on_delete=models.CASCADE) 

class Updates(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(default='Новое обновление')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)