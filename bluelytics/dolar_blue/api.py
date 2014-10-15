from django.http import HttpResponse
import json, datetime

from decimal import Decimal 

from dolar_blue.utils import DecimalEncoder, arg
from dolar_blue.calculations import maxSources, maxSourcesYesterday, convDolar

def api_dolar(d):
  return {'date': d.date.astimezone(arg).isoformat(),
        'compra': d.value_buy,
        'venta': d.value_sell,
        'name': d.source.source,
        'long_name': d.source.description}


def avgBlue(input):
  i = 0
  v = 0
  c = 0
  d = 0
  for b in input:
    if b['name'] != 'oficial':
      i+=1
      v+=b['venta']
      c+=b['compra']
  return {'date': datetime.datetime.now().isoformat(),
        'compra': c/i,
        'venta': v/i,
        'name': 'blue',
        'long_name': 'Bluelytics'
          }

def addOficial(input, perc, newname):
  mult = (100 + perc) / Decimal(100)
  print mult
  for b in input:
    if b['name'] == 'oficial':
      return {'date': b['date'],
        'compra': b['compra'] * mult,
        'venta':  b['venta'] * mult,
        'name': 'oficial_' + str(perc),
        'long_name': newname
          }

def lastprice(request):
  max_sources = map(api_dolar, maxSources())
  max_sources_yesterday = map(api_dolar, maxSourcesYesterday())

  max_sources.append(avgBlue(max_sources))
  max_sources_yesterday.append(avgBlue(max_sources_yesterday))

  max_sources.append(addOficial(max_sources, 20, 'Oficial Ahorro'))
  max_sources_yesterday.append(addOficial(max_sources_yesterday, 20, 'Oficial Ahorro'))

  max_sources.append(addOficial(max_sources, 35, 'Oficial Tarjeta'))
  max_sources_yesterday.append(addOficial(max_sources_yesterday, 35, 'Oficial Tarjeta'))

  output = {'Today': max_sources , 'Yesterday': max_sources_yesterday}
  return HttpResponse(json.dumps(output, cls=DecimalEncoder), mimetype="application/json")
