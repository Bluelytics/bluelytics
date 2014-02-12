from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
from django.db.models import Max, Min
import json, pytz

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg

def maxSources():
  all_sources = Source.objects.all()
  maxSources = []
  for src in all_sources:
    record = DolarBlue.objects.filter(source__exact=src).order_by('-date').first()
    maxSources.append(record)

  return maxSources


def index(request):
  timezone.activate(pytz.timezone("America/Argentina/Buenos_Aires"))
  max_sources = map(convDolar, maxSources())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())
  context = { 'max_sources': json.dumps(max_sources, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources) }

  return render(request, 'index.html', context)

def json_lastprice(request):
  max_sources = map(convDolar, maxSources())
  return HttpResponse(max_sources, mimetype="application/json")

def convDolar(e):
  return {'date': e.date.astimezone(arg).strftime("%d/%m/%Y %H:%M:%S"),
        'value_buy': e.value_buy,
        'value_sell': e.value_sell,
        'value_avg': e.value_avg,
        'source': e.source.source}

def blue_graph(request):
  all_prices = map(convDolar, DolarBlue.objects.all())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())

  context = { 'all_prices': json.dumps(all_prices, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources) }

  return render(request, 'graph.html', context)