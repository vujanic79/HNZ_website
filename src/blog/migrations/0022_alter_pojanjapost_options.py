# Generated by Django 5.1 on 2024-08-27 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_pojanjapost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pojanjapost',
            options={'ordering': ['-album', '-title']},
        ),
    ]
