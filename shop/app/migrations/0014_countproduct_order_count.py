# Generated by Django 4.2.17 on 2024-12-17 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_messagemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='count',
            field=models.ManyToManyField(to='app.countproduct'),
        ),
    ]
