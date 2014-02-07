from django.shortcuts import render

from dolar_blue.models import DolarBlue

def index(request):
    #last_prices = DolarBlue.objects.order_by('-date')[:30]
    last_price = DolarBlue.objects.order_by('-date').last()
    context = { 'last_price': last_price }

    return render(request, 'index.html', context)