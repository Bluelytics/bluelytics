from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
import json, pytz

from dolar_blue.models import DolarBlue
from dolar_blue.utils import DecimalEncoder, arg

def lastPrice():
  return DolarBlue.objects.last()

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
        'value_avg': e.value_avg}

def blue_graph(request):
  all_prices = DolarBlue.objects.all()
  all_prices_dict = map(convDolar, all_prices)

  context = { 'all_prices': json.dumps(all_prices_dict, cls=DecimalEncoder) }

  return render(request, 'graph.html', context)