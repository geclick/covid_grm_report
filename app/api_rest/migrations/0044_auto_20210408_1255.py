# Generated by Django 2.2.16 on 2021-04-08 16:55

import api_rest.utils
from django.db import migrations
import protected_media.models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0043_merge_20210408_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epidemiologiauploadmodel',
            name='archivo',
            field=protected_media.models.ProtectedFileField(storage=protected_media.models.ProtectedFileSystemStorage(), upload_to=api_rest.utils.epidemiologia_directory_path),
        ),
        migrations.AlterField(
            model_name='higieneuploadmodel',
            name='archivo',
            field=protected_media.models.ProtectedFileField(storage=protected_media.models.ProtectedFileSystemStorage(), upload_to=api_rest.utils.higiene_directory_path),
        ),
        migrations.AlterField(
            model_name='resultmodel',
            name='archivo',
            field=protected_media.models.ProtectedFileField(storage=protected_media.models.ProtectedFileSystemStorage(), upload_to=api_rest.utils.lab_directory_path, verbose_name='Archivo Excel'),
        ),
    ]
