from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars')
    password = models.CharField(max_length=128)
    # password1 = models.CharField(max_length=128)
    # password2 = models.CharField(max_length=128)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set', # Изменение related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set', # Изменение related_name
    )

    def __str__(self):
        return self.username 

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user_initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiator')
    user_recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)