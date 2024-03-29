# Generated by Django 5.0.2 on 2024-03-03 18:19

from django.db import migrations


def add_email_to_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    for user in User.objects.all():
        if not user.email:
            user.email = 'crazydealer2003@gmail.com'  # Set a default email
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('html_parser', '0003_transaction_volume'),
    ]

    operations = [
        migrations.RunPython(add_email_to_existing_users),
    ]
