# Generated by Django 5.1 on 2024-08-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20240807_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.FileField(blank=True, null='', upload_to='image/'),
        ),
    ]
