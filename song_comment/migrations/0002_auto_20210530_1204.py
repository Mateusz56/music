# Generated by Django 3.1.7 on 2021-05-30 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songcomment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 12, 4, 19, 753386)),
        ),
    ]
