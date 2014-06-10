from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
from django.db.models import Max, Min
import json, pytz

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg
from dolar_blue.calculations import maxSources, maxSourcesYesterday, convDolar

def last_price_each_day():
  return DolarBlue.objects.raw('\
  select db.*\
  from dolar_blue_dolarblue db\
  inner join\
    (select source_id, max(date) as date, date(date) as datepart\
      from dolar_blue_dolarblue\
      group by source_id, date(date)\
    ) dbj\
  on db.source_id = dbj.source_id and db.date = dbj.date\
  order by db.date;\
  ')



def index(request):
  timezone.activate(pytz.timezone("America/Argentina/Buenos_Aires"))
  max_sources = map(convDolar, maxSources())
  max_sources_yesterday = map(convDolar, maxSourcesYesterday())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())
  context = { 'max_sources': json.dumps(max_sources, cls=DecimalEncoder),
              'max_sources_yesterday': json.dumps(max_sources_yesterday, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources) }

  return render(request, 'index.html', context)

def json_index(request):
  return render(request, 'json.html', {})

def json_lastprice(request):
  max_sources = map(convDolar, maxSources())
  return HttpResponse(json.dumps(max_sources, cls=DecimalEncoder), mimetype="application/json")


def blue_graph(request):
  all_prices = map(convDolar, last_price_each_day())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())

  context = { 'all_prices': json.dumps(all_prices, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources) }

  return render(request, 'graph.html', context)

def wordcloud(request):
  return render(request, 'wordcloud.html', {})

def forecast(request):
  return render(request, 'forecast.html', {})


def gap(request):
  all_prices = map(convDolar, last_price_each_day())
  timezone.activate(pytz.timezone("America/Argentina/Buenos_Aires"))
  max_sources = map(convDolar, maxSources())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())
  context = { 'max_sources': json.dumps(max_sources, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources),
              'all_prices': json.dumps(all_prices, cls=DecimalEncoder) }

  return render(request, 'gap.html', context)