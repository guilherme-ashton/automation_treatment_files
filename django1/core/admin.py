from django.contrib import admin
from .models import Alarme, Objeto, Configuracao


class AlarmeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'alarme_objeto', )




class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('severity', 'alarme')


admin.site.register(Alarme, AlarmeAdmin)
admin.site.register(Objeto, ObjetoAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)


