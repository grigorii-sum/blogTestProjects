# Generated by Django 3.1.7 on 2021-03-24 09:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0011_auto_20210324_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='readers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
