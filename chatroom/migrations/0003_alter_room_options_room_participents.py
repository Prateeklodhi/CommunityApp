# Generated by Django 4.0.2 on 2022-07-08 11:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatroom', '0002_auto_20220619_1351'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-update', '-created']},
        ),
        migrations.AddField(
            model_name='room',
            name='participents',
            field=models.ManyToManyField(related_name='participents', to=settings.AUTH_USER_MODEL),
        ),
    ]
