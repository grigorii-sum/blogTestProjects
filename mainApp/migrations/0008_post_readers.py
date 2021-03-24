# Generated by Django 3.1.7 on 2021-03-24 08:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0007_auto_20210323_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='readers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
