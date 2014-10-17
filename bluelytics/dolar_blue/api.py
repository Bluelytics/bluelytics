from django.http import HttpResponse
import json, datetime

from operator import itemgetter
from decimal import Decimal 

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg
from dolar_blue.calculations import maxCurrencies, convCurr

def api_dolar(d):
  return {'date': d.date.astimezone(arg).isoformat(),
        'compra': d.value_buy,
        'venta': d.value_sell,
        'name': d.source.source,
        'long_name': d.source.description}

def all_prices():
  all_sources = Source.objects.all()
  allPrices = []
  for src in all_sources:
    today = DolarBlue.objects.filter(source__exact=src).order_by('-date').first()
    dateCalc = today.date.replace(hour=3, minute=0, second=0)
    yesterday = DolarBlue.objects.filter(source__exact=src, date__lt=dateCalc).order_by('-date').first()

    allPrices.append({
      'date': today.date.astimezone(arg).isoformat(),
      'compra': today.value_buy,
      'venta': today.value_sell,
      'compra_ayer': yesterday.value_buy,
      'venta_ayer': yesterday.value_sell,
      'name': today.source.source,
      'long_name': today.source.description
      })

  return allPrices

def avgBlue(input):
  i = 0
  v = 0
  c = 0
  c_a = 0
  v_a = 0
  d = 0
  for b in input:
    if b['name'] != 'oficial':
      i+=1
      v+=b['venta']
      c+=b['compra']
      v_a+=b['venta_ayer']
      c_a+=b['compra_ayer']
  return {'date': datetime.datetime.now().isoformat(),
        'compra': c/i,
        'venta': v/i,
        'compra_ayer': c_a/i,
        'venta_ayer': v_a/i,
        'name': 'blue',
        'long_name': 'Dolar Blue'
          }

def addOficial(input, perc, newname):
  mult = (100 + perc) / Decimal(100)
  print mult
  for b in input:
    if b['name'] == 'oficial':
      return {'date': b['date'],
        'compra': b['compra'] * mult,
        'venta':  b['venta'] * mult,
        'compra_ayer': b['compra_ayer'] * mult,
        'venta_ayer':  b['venta_ayer'] * mult,
        'name': 'oficial_' + str(perc),
        'long_name': newname
          }


def lastprice(request):
  allPrices = all_prices()

  output = []

  output.append(avgBlue(allPrices))

  output+=allPrices

  output.append(addOficial(allPrices, 20, 'Oficial Ahorro'))

  output.append(addOficial(allPrices, 35, 'Oficial Tarjeta'))

  return HttpResponse(json.dumps(output, cls=DecimalEncoder), mimetype="application/json")

def all_currencies(request):
  max_currencies = map(convCurr, maxCurrencies())
  max_currencies.sort(key=itemgetter('code'))

  return HttpResponse(json.dumps(max_currencies, cls=DecimalEncoder), mimetype="application/json")