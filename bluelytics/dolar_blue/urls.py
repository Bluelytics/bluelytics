from django.conf.urls import patterns, url

from dolar_blue import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^json/last_price$', views.json_lastprice, name='json_lastprice')
)