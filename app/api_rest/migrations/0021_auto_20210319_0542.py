# Generated by Django 2.2.16 on 2021-03-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0020_auto_20210319_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datahigienemodel',
            name='ci_pasaporte',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='CI o Pasaporte'),
        ),
    ]
