# Generated by Django 3.1.6 on 2021-07-29 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireMap', '0003_auto_20210717_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incendio',
            name='activo',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incendio',
            name='bomberos_afectados',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incendio',
            name='riesgo_interfase',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incendio',
            name='unid_livianas_afectadas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incendio',
            name='unid_pesadas_afectadas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
