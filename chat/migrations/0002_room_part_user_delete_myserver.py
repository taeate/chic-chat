# Generated by Django 4.0.1 on 2022-01-17 09:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='part_user',
            field=models.ManyToManyField(related_name='part_server', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='MyServer',
        ),
    ]