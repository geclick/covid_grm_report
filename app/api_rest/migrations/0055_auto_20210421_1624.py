# Generated by Django 2.2.16 on 2021-04-21 20:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0054_auto_20210421_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 21, 16, 24, 31, 720222), verbose_name='Fecha del resultado'),
        ),
    ]
