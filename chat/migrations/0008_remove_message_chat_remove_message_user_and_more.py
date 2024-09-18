# Generated by Django 5.1 on 2024-09-10 07:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0007_chatuser"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="chat",
        ),
        migrations.RemoveField(
            model_name="message",
            name="user",
        ),
        migrations.AlterField(
            model_name="message",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
