# Generated by Django 5.1.4 on 2024-12-18 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_alter_sell_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
