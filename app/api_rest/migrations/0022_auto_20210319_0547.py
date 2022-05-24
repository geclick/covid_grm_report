# Generated by Django 2.2.16 on 2021-03-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0021_auto_20210319_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datahigienemodel',
            name='ct',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='CT'),
        ),
        migrations.AlterField(
            model_name='datahigienemodel',
            name='resultado',
            field=models.CharField(blank=True, default='Pendiente', max_length=255, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='datahigienemodel',
            name='sexo',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Sexo'),
        ),
        migrations.AlterField(
            model_name='datahigienemodel',
            name='tipo_muestra',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tipo de muestreo'),
        ),
    ]