# Generated by Django 5.0.1 on 2024-01-22 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0006_alter_categoryitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активность объявления'),
        ),
    ]