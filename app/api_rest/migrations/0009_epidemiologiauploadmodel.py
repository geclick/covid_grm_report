# Generated by Django 2.2.16 on 2021-03-15 03:11

import api_rest.utils
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0008_auto_20210315_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='EpidemiologiaUploadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('archivo', models.FileField(upload_to=api_rest.utils.epidemiologia_directory_path)),
            ],
            options={
                'verbose_name': 'Archivo de epidemiologia',
                'verbose_name_plural': 'Archivoa de epidemiologia',
                'ordering': ['fecha'],
            },
        ),
    ]
