# Generated by Django 4.1.7 on 2023-03-09 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
