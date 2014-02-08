from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
import pytz

from dolar_blue.models import DolarBlue

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