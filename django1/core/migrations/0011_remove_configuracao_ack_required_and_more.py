# Generated by Django 4.0.3 on 2022-05-18 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_configuracao_latched'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracao',
            name='ack_required',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='alarm_class',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='alarme',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='factory',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='input_tag',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='minimum_duration',
        ),
        migrations.RemoveField(
            model_name='configuracao',
            name='show_alarm',
        ),
    ]