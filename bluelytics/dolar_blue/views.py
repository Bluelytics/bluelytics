from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
from django.db.models import Max, Min
import json, pytz

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg

def lastPrice():
  all_sources = Source.objects.all()
  maxSources = []
  for src in all_sources:
    record = DolarBlue.objects.filter(source__exact=src).order_by('-date')[:1].last()
    maxSources.append(record)

  lp={
    'date':max([r.date for r in maxSources]),
    'value_buy':sum([r.value_buy for r in maxSources])/len(maxSources),
    'value_sell':sum([r.value_sell for r in maxSources])/len(maxSources),
    'value_avg':sum([r.value_avg for r in maxSources])/len(maxSources)
  }

  return lp

def index(request):
  timezone.activate(pytz.timezone("America/Argentina/Buenos_Aires"))
  last_price = lastPrice()
  context = { 'last_price': last_price }

  return render(request, 'index.html', context)

def json_lastprice(request):
  last_price = lastPrice().json()
  return HttpResponse(last_price, mimetype="application/json")

def convDolar(e):
  return {'date': e.date.astimezone(arg).strftime("%d/%m/%Y %H:%M:%S"),
        'value_buy': e.value_buy,
        'value_sell': e.value_sell,
        'value_avg': e.value_avg,
        'source': e.source.source}

def blue_graph(request):
  all_prices = DolarBlue.objects.all()
  all_prices_dict = map(convDolar, all_prices)
  all_sources = map(lambda x: x.source,Source.objects.all())

  context = { 'all_prices': json.dumps(all_prices_dict, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources) }

  return render(request, 'graph.html', context)