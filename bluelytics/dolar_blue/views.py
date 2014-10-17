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


def index(request):
  timezone.activate(pytz.timezone("America/Argentina/Buenos_Aires"))
  max_sources = map(convDolar, maxSources())
  max_sources_yesterday = map(convDolar, maxSourcesYesterday())
  all_sources = map(lambda x: {"name":x.source, "description":x.description},Source.objects.all())
  context = { 'max_sources': json.dumps(max_sources, cls=DecimalEncoder),
              'max_sources_yesterday': json.dumps(max_sources_yesterday, cls=DecimalEncoder),
              'all_sources': json.dumps(all_sources) }

  return render(request, 'index.html', context)