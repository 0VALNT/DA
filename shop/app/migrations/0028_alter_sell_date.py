# Generated by Django 5.1.4 on 2024-12-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_sell'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='date',
            field=models.DateField(),
        ),
    ]
