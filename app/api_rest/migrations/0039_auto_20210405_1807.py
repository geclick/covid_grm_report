# Generated by Django 2.2.16 on 2021-04-05 22:07

import api_rest.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0038_centroaislamiento_municipio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='archivo',
            field=models.FileField(upload_to=api_rest.utils.lab_directory_path, verbose_name='Archivo Excel'),
        ),
    ]
