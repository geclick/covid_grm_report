# Generated by Django 2.2.16 on 2021-04-19 02:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0049_auto_20210418_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 22, 1, 3, 152998), verbose_name='Fecha del resultado'),
        ),
    ]