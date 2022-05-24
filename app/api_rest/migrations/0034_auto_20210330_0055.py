# Generated by Django 2.2.16 on 2021-03-30 04:55

import api_rest.utils
import api_rest.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0033_auto_20210329_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epidemiologiauploadmodel',
            name='archivo',
            field=models.FileField(upload_to=api_rest.utils.epidemiologia_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), api_rest.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='higieneuploadmodel',
            name='archivo',
            field=models.FileField(upload_to=api_rest.utils.higiene_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), api_rest.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='resultmodel',
            name='archivo',
            field=models.FileField(upload_to=api_rest.utils.lab_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), api_rest.validators.validate_file_size], verbose_name='Archivo Excel'),
        ),
    ]
