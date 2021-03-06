# Generated by Django 2.2.16 on 2021-03-27 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0029_auto_20210325_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=255)),
                ('result_date', models.DateField(auto_now_add=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api_rest.DataEpidemiologiaModel')),
            ],
            options={
                'verbose_name': 'Registro de resultados de una muestra',
                'verbose_name_plural': 'Registro de resultados de una muestra',
            },
        ),
    ]
