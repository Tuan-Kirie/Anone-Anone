# Generated by Django 3.0.3 on 2020-04-01 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200401_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readstatus',
            name='profile',
        ),
        migrations.AddField(
            model_name='profile',
            name='read_status',
            field=models.ManyToManyField(default=None, null=True, related_name='status', to='users.ReadStatus'),
        ),
    ]
