# Generated by Django 4.0.3 on 2022-05-24 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_alarme_alarme_bit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuracao',
            old_name='Input Tag (bit)',
            new_name='input_tag',
        ),
    ]
