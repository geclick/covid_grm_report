# Generated by Django 2.2.16 on 2021-03-31 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0033_auto_20210330_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataepidemiologiamodel',
            options={'ordering': ['pk'], 'verbose_name': 'Base de datos de resultado', 'verbose_name_plural': 'Base de datos de resultados'},
        ),
    ]