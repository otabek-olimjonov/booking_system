# Generated by Django 4.1.2 on 2024-10-07 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0004_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='user_id',
            new_name='user',
        ),
    ]
