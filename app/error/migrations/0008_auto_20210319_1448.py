# Generated by Django 2.2.16 on 2021-03-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0007_auto_20210319_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataepidemiologiaerror',
            name='sexo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sexo'),
        ),
    ]