# Generated by Django 3.1 on 2020-09-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedad',
            name='youtube',
            field=models.TextField(blank=True, null=True),
        ),
    ]
