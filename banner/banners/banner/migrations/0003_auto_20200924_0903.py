# Generated by Django 3.1 on 2020-09-24 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_auto_20200923_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='imagen',
            field=models.ImageField(upload_to='banners'),
        ),
    ]