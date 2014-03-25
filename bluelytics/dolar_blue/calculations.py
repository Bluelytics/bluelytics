from dolar_blue.models import DolarBlue, Source, Currency, CurrencyValue
from dolar_blue.utils import arg

import datetime
from datetime import timedelta


def maxSourcesYesterday():
  all_sources = Source.objects.all()
  maxSources = []
  for src in all_sources:
    last = DolarBlue.objects.filter(source__exact=src).order_by('-date').first()

    dateCalc = last.date.replace(hour=3, minute=0, second=0)

    record = DolarBlue.objects.filter(source__exact=src, date__lt=dateCalc).order_by('-date').first()
    maxSources.append(record)

  return maxSources

def maxSources():
  all_sources = Source.objects.all()
  maxSources = []
  for src in all_sources:
    record = DolarBlue.objects.filter(source__exact=src).order_by('-date').first()
    maxSources.append(record)

  return maxSources

def convDolar(e):
  return {'date': e.date.astimezone(arg).isoformat(),
        'value_buy': e.value_buy,
        'value_sell': e.value_sell,
        'value_avg': e.value_avg,
        'source': e.source.source}

def maxCurrencies():
  all_currencies = Currency.objects.all()
  maxCurrencies = []
  for cur in all_currencies:
    record = CurrencyValue.objects.filter(curr__exact=cur).order_by('-date').first()
    maxCurrencies.append(record)

  return maxCurrencies

def convCurr(e):
  return {'value': e.value,
        'code': e.curr.code,
        'name': e.curr.name}