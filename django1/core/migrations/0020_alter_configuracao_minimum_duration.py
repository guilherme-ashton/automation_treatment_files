# Generated by Django 4.0.3 on 2022-05-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_configuracao_ak_tag_configuracao_all_levels_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracao',
            name='minimum_duration',
            field=models.DecimalField(decimal_places=2, help_text='Seconds', max_digits=8),
        ),
    ]
