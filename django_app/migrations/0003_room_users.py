# Generated by Django 5.0.1 on 2024-01-19 23:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0002_room'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(max_length=50, to=settings.AUTH_USER_MODEL, verbose_name='Участники чата'),
        ),
    ]
