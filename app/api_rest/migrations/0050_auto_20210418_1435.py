# Generated by Django 2.2.16 on 2021-04-18 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0049_auto_20210418_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 14, 35, 31, 383105), verbose_name='Fecha del resultado'),
        ),
    ]
