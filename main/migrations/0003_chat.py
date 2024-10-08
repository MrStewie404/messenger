# Generated by Django 3.2.6 on 2024-08-29 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20240828_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiator', to=settings.AUTH_USER_MODEL)),
                ('user_recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
