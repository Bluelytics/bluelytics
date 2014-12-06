from django.conf.urls import patterns, url

from dolar_blue import views, api, new_api

urlpatterns = patterns('',
    url(r'^json/last_price$', views.json_lastprice, name='json_lastprice'),

    url(r'^v2/latest$', new_api.latest, name='latest'),

    url(r'^api/last_price$', api.lastprice, name='api_lastprice'),
    url(r'^api/all_currencies$', api.all_currencies, name='api_all_currencies')
)
