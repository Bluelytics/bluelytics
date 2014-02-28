from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
from django.db.models import Max, Min
import json, pytz

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg
from dolar_blue.calculations import maxSources, maxCurrencies, convDolar, convCurr

def calculator(request):
  timezone.activate(pytz.timezone("America/Argentina/Buenos_Aires"))
  max_sources = map(convDolar, maxSources())
  max_currencies = map(convCurr, maxCurrencies())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())
  context = { 'max_sources': json.dumps(max_sources, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources),
              'max_currencies': json.dumps(max_currencies, cls=DecimalEncoder) }

  return render(request, 'calculator.html', context)