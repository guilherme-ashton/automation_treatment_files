# Generated by Django 4.0.3 on 2022-05-24 18:12

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_configuracao_minimum_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarme',
            name='alarme_bit',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='input_tag',
        ),
        migrations.AddField(
            model_name='configuracao',
            name='Input Tag (bit)',
            field=models.CharField(default=1, max_length=50, verbose_name=core.models.Alarme),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Bit',
        ),
    ]
