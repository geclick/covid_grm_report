# Generated by Django 2.2.16 on 2021-04-21 03:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0052_auto_20210419_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 20, 23, 39, 14, 164792), verbose_name='Fecha del resultado'),
        ),
    ]
