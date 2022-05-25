# Generated by Django 4.0.3 on 2022-05-17 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_objeto_alarme_padrao_alter_objeto_bit_padrao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objeto',
            name='alarme_padrao',
        ),
        migrations.RemoveField(
            model_name='objeto',
            name='bit_padrao',
        ),
        migrations.AddField(
            model_name='alarme',
            name='alarme_padrao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alarme_padrao', to='core.objeto'),
        ),
        migrations.AddField(
            model_name='bit',
            name='bit_padrao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bit_padrao', to='core.objeto'),
        ),
    ]
