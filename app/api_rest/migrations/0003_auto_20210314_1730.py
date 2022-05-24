# Generated by Django 2.2.16 on 2021-03-14 17:30

import api_rest.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0002_auto_20210313_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='dataepidemiologiamodel',
            name='no_pcr_realizado',
            field=models.IntegerField(blank=True, null=True, verbose_name='No PCR'),
        ),
        migrations.CreateModel(
            name='ResultModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to=api_rest.utils.lab_directory_path)),
                ('laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api_rest.Laboratorio')),
            ],
        ),
    ]
