# Generated by Django 3.1.7 on 2021-05-28 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0002_auto_20210405_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='genre',
            field=models.CharField(choices=[('Pop', 'Pop'), ('Rock', 'Rock'), ('Folk', 'Folk'), ('Metal', 'Metal'), ('Other', 'Other')], default='Other', max_length=20),
        ),
    ]
