# Generated by Django 4.0.3 on 2022-05-19 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_configuracao_cfg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracao',
            name='alarme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarme', to='core.alarme'),
        ),
    ]