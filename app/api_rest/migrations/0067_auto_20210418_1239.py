# Generated by Django 2.2.16 on 2021-04-18 16:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0066_auto_20210418_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 12, 39, 4, 977400), verbose_name='Fecha del resultado'),
        ),
    ]
