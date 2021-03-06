# Generated by Django 2.2.16 on 2021-04-14 14:25

import api_rest.utils
import datetime
from django.db import migrations, models
import protected_media.models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0045_auto_20210409_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='archivo',
            field=protected_media.models.ProtectedFileField(storage=protected_media.models.ProtectedFileSystemStorage(), upload_to=api_rest.utils.lab_directory_path),
        ),
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 14, 10, 25, 12, 773803), verbose_name='Fecha del resultado'),
        ),
    ]
