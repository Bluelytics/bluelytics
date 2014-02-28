from django.conf.urls import patterns, url

from dolar_blue import views
from dolar_blue import calculator_view

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^graph$', views.blue_graph, name='blue_graph'),
    url(r'^wordcloud$', views.wordcloud, name='wordcloud'),
    url(r'^gap$', views.gap, name='gap'),
    url(r'^calc$', calculator_view.calculator, name='calculator'),
    url(r'^json/last_price$', views.json_lastprice, name='json_lastprice')
)