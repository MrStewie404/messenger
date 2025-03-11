from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Avatars(models.Model):
    path = models.ImageField(upload_to='static/media/avatars/', 
                             default='static/media/avatars/default.png')
    user = models.ForeignKey(User, related_name='avatars', on_delete=models.CASCADE) 

class UserSupplement(models.Model):
    user = models.ForeignKey(User, related_name='description', on_delete=models.CASCADE)
    description = models.TextField(default='Описание')

    def __str__(self):
        return self.description

class Modules(models.Model):
    id = models.AutoField(verbose_name='id', primary_key=True, auto_created=True)
    name = models.TextField(verbose_name='name')
    description = models.TextField(verbose_name='description')
    path = models.FileField(verbose_name='path', upload_to='static/media/modules/', default='static/media/modules/default/profile.html')
    user = models.ForeignKey(User, related_name='modules', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name='date', default=timezone.now)
    visible_in_public = models.BooleanField(default=False)
    verificated = models.BooleanField(verbose_name='check', default=False)
    
    def __str__(self):
        return self.name

class AddedModules(models.Model):
    module = models.ForeignKey(Modules, verbose_name='module', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    visibility_for_others = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.module.name
    
class ModuleSequence(models.Model):
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    modules_id = models.JSONField('Modules sequence', default=list, null=False)

class Updates(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(default='Новое обновление')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)