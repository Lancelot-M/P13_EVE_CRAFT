# Generated by Django 3.2 on 2021-04-28 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crafts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='groups_list',
        ),
        migrations.RemoveField(
            model_name='group',
            name='types_list',
        ),
    ]