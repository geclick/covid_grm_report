# Generated by Django 2.2.16 on 2021-03-16 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0014_auto_20210315_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datahigienemodel',
            options={'ordering': ['codigo'], 'verbose_name': 'Dato de higiene', 'verbose_name_plural': 'Datos de higiene'},
        ),
    ]