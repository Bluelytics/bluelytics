from django.conf.urls import patterns, url

from dolar_blue import views, calculator_view, api

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^graph$', views.blue_graph, name='blue_graph'),
    url(r'^wordcloud$', views.wordcloud, name='wordcloud'),
    url(r'^forecast$', views.forecast, name='forecast'),
    url(r'^gap$', views.gap, name='gap'),
    url(r'^calc$', calculator_view.calculator, name='calculator'),
    url(r'^json$', views.json_index, name='json'),
    url(r'^json/last_price$', views.json_lastprice, name='json_lastprice'),
    
    url(r'^api/last_price$', api.lastprice, name='api_lastprice')
)