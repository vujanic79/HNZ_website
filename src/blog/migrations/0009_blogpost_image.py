# Generated by Django 2.2 on 2024-08-07 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20240807_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.FileField(blank=True, null='', upload_to='image/'),
        ),
    ]
