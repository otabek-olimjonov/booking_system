# Generated by Django 4.1.2 on 2024-10-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingspot',
            name='door',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='parkingspot',
            name='status',
            field=models.CharField(choices=[('free', 'Free'), ('booked', 'Booked'), ('in_use', 'In Use')], max_length=10),
        ),
    ]
