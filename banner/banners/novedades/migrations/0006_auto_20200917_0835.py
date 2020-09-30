# Generated by Django 3.1 on 2020-09-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0005_auto_20200916_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novedad',
            name='ID_youtube',
        ),
        migrations.RemoveField(
            model_name='novedad',
            name='youtube',
        ),
        migrations.AddField(
            model_name='novedad',
            name='youtube_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='novedad',
            name='youtube_video_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
