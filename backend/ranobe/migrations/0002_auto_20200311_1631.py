# Generated by Django 3.0.3 on 2020-03-11 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ranobe', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapters',
            options={'ordering': ['id']},
        ),
    ]
