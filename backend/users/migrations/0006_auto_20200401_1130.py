# Generated by Django 3.0.3 on 2020-04-01 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200401_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='books_stat',
            new_name='read_status',
        ),
    ]
