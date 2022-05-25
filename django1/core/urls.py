from django.conf import settings
from django.urls import path, re_path
from django import views
from django.conf.urls.static import static
from django.views.static import serve
from .views import adicionaArquivoXml, adicionaArquivoL5X, adicionaArquivoLvu, adicionaIntlk
from django.contrib import admin

urlpatterns = [
    path('', adicionaArquivoXml, name='index'),
    #path('download-file', downloadTelastag, name='download-file'),
    path('l5x', adicionaArquivoL5X, name='l5x'),
    #path('download-l5x', downloadL5X, name='download-l5x'),
    path('lvu', adicionaArquivoLvu, name='lvu'),
    #path('download-lvu', downloadLVU, name='download-lvu'),
    path('intlk', adicionaIntlk, name='intlk'),
    #path('download-intlk', downloadIntlk, name='download-intlk'),

]

"""re_path(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
# path('contato', contato, name='contato'),
# path('lotes/<int:pk>', lotes, name= 'lotes'),


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""