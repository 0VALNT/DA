# Generated by Django 4.2.17 on 2024-12-15 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_message_room_remove_message_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]