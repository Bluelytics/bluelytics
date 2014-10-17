from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
from django.db.models import Max, Min
import json, pytz

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg
from dolar_blue.calculations import maxSources, maxSourcesYesterday, convDolar


def json_lastprice(request):
  max_sources = map(convDolar, maxSources())
  return HttpResponse(json.dumps(max_sources, cls=DecimalEncoder), mimetype="application/json")

