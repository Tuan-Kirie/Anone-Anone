# Generated by Django 3.0.3 on 2020-03-16 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranobe', '0002_auto_20200311_1631'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='text',
            field=models.TextField(default=' ', max_length=600),
        ),
        migrations.AlterField(
            model_name='comments',
            name='ranobe',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ranobe.Ranobe'),
        ),
    ]
