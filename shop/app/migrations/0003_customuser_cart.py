# Generated by Django 5.1.4 on 2024-12-12 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cart',
            field=models.ManyToManyField(to='app.product'),
        ),
    ]
