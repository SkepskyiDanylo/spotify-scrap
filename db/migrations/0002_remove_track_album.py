# Generated by Django 4.0.2 on 2024-09-21 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='album',
        ),
    ]
