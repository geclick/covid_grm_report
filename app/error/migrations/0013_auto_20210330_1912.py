# Generated by Django 2.2.16 on 2021-03-30 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0012_auto_20210324_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataepidemiologiaerror',
            options={'verbose_name': 'Error de procesamiento de archivo             de restauración de resultados', 'verbose_name_plural': 'Error de procesamiento de archivos             de restauración de resultados'},
        ),
        migrations.AlterModelOptions(
            name='datahigieneerror',
            options={'verbose_name': 'Error de procesamiento de archivo de muestra', 'verbose_name_plural': 'Errores de procesamiento de archivo de muestras'},
        ),
        migrations.AlterModelOptions(
            name='placaerrormodel',
            options={'verbose_name': 'Error de procesamiento de archivo de resultados', 'verbose_name_plural': 'Errores de procesamiento de             archivos de resultados'},
        ),
    ]
