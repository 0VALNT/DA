# Generated by Django 5.1.4 on 2024-12-18 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_sell_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sell',
            old_name='time',
            new_name='date',
        ),
    ]
