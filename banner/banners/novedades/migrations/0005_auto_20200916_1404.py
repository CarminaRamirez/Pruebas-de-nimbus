# Generated by Django 3.1 on 2020-09-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0004_auto_20200916_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novedad',
            name='link_youtube',
        ),
        migrations.AddField(
            model_name='novedad',
            name='ID_youtube',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='youtube',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
