# Generated by Django 2.2.16 on 2021-04-18 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0051_auto_20210418_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 14, 42, 35, 773714), verbose_name='Fecha del resultado'),
        ),
    ]
