# Generated by Django 2.2.16 on 2021-03-17 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0014_auto_20210315_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Resultado de prueba PCR',
                'verbose_name_plural': 'Resultado de prueba PCR',
            },
        ),
        migrations.AlterModelOptions(
            name='datahigienemodel',
            options={'ordering': ['codigo'], 'verbose_name': 'Dato de higiene', 'verbose_name_plural': 'Datos de higiene'},
        ),
    ]
