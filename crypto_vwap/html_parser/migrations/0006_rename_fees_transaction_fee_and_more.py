# Generated by Django 5.0.2 on 2024-03-12 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('html_parser', '0005_auto_20240303_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='fees',
            new_name='fee',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='filled',
            new_name='quantity',
        ),
    ]
