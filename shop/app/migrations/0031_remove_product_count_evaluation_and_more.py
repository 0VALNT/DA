# Generated by Django 5.1.4 on 2024-12-18 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_product_count_evaluation_product_numm_evaluation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='count_evaluation',
        ),
        migrations.RemoveField(
            model_name='product',
            name='numm_evaluation',
        ),
        migrations.DeleteModel(
            name='Evaluation',
        ),
    ]
