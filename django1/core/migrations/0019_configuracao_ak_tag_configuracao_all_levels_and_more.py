# Generated by Django 4.0.3 on 2022-05-19 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_configuracao_alarme'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracao',
            name='ak_tag',
            field=models.CharField(default=1, max_length=100, verbose_name='Acknowledged Tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='all_levels',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='disable_tag',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='disable_tag2',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='enable_tag',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='in_alarm',
            field=models.CharField(default=1, max_length=100, verbose_name='In Alarm Tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='shelve_duration',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='shelved_tag',
            field=models.CharField(default=1, max_length=100, verbose_name='Shelved Tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='suppressed_tag',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='supress_tag',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='unshelve',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100, verbose_name='Unshelve All Tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracao',
            name='unsuppress_tag',
            field=models.CharField(default=1, help_text='Control Tags', max_length=100),
            preserve_default=False,
        ),
    ]
