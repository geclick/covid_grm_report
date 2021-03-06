# Generated by Django 2.2.16 on 2021-04-18 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_server_access_logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesslogsmodel',
            options={'verbose_name': 'Log de Acceso', 'verbose_name_plural': 'Logs de Accesos'},
        ),
        migrations.AlterField(
            model_name='accesslogsmodel',
            name='data',
            field=models.TextField(blank=True, null=True, verbose_name='Datos'),
        ),
        migrations.AlterField(
            model_name='accesslogsmodel',
            name='ip_address',
            field=models.CharField(blank=True, max_length=45, verbose_name='Dirección IP'),
        ),
        migrations.AlterField(
            model_name='accesslogsmodel',
            name='method',
            field=models.CharField(blank=True, max_length=8, verbose_name='Método'),
        ),
        migrations.AlterField(
            model_name='accesslogsmodel',
            name='path',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Ruta'),
        ),
        migrations.AlterField(
            model_name='accesslogsmodel',
            name='referrer',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Referencia'),
        ),
        migrations.AlterField(
            model_name='accesslogsmodel',
            name='timestamp',
            field=models.DateTimeField(blank=True, verbose_name='Fecha y Hora'),
        ),
    ]
