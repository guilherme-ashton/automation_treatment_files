from django.db import models

class Objeto(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome


class Alarme(models.Model):
    nome = models.CharField(max_length=50)
    alarme_objeto = models.ForeignKey(Objeto, related_name='alarme_objeto',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome


class Configuracao(models.Model):

    condition_choices = (
        ('0', 0),
        ('1', 1)
    )

    alarme= models.ForeignKey(Alarme, related_name='alarme',on_delete=models.CASCADE)
    input_tag = models.CharField('input_tag(bit)', max_length=100)
    condition =models.CharField('Condition', max_length=50, choices= condition_choices)
    severity = models.CharField( 'Severity', max_length=50)
    latched = models.BooleanField('Latched')
    ak_required = models.BooleanField('Acknowledge required')
    show_alarm= models.BooleanField('Show Alarm as a Tag')
    minimum_duration = models.DecimalField(max_digits=8, decimal_places=2, help_text= 'Seconds')
    alarm_class = models.CharField('Alarm Class', max_length=50)
    factory = models.CharField('Factory Talk View Command', max_length=100)
    disable_tag = models.CharField(max_length=100)
    suppressed_tag = models.CharField(max_length=100)
    in_alarm = models.CharField('In Alarm Tag', max_length=100)
    ak_tag =  models.CharField('Acknowledged Tag', max_length=100)
    shelved_tag =  models.CharField('Shelved Tag', max_length=100)
    disable_tag2 = models.CharField(max_length=100, help_text='Control Tags')
    enable_tag = models.CharField(max_length=100, help_text='Control Tags')
    supress_tag= models.CharField(max_length=100, help_text='Control Tags')
    unsuppress_tag = models.CharField(max_length=100, help_text='Control Tags')
    all_levels = models.CharField(max_length=100, help_text='Control Tags')
    shelve_duration = models.CharField(max_length=100, help_text='Control Tags')
    unshelve = models.CharField('Unshelve All Tag',max_length=100, help_text='Control Tags')

    def __str__(self):
        return self.severity

    class Meta:
        verbose_name= 'Configuração'
        verbose_name_plural = 'Configurações'


