# Generated by Django 2.2.16 on 2021-04-18 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0065_auto_20210418_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 12, 31, 56, 265289), verbose_name='Fecha del resultado'),
        ),
    ]
