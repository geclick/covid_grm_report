# Generated by Django 2.2.16 on 2021-04-18 21:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0047_auto_20210414_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultmodel',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 17, 22, 22, 234410), verbose_name='Fecha del resultado'),
        ),
    ]
