# Generated by Django 2.2.16 on 2021-03-31 14:02

import api_rest.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0034_auto_20210330_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epidemiologiauploadmodel',
            name='archivo',
            field=models.FileField(upload_to=api_rest.utils.epidemiologia_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'])]),
        ),
    ]
