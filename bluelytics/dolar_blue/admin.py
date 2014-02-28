from django.contrib import admin

from dolar_blue.models import DolarBlue, Source, Currency, CurrencyValue

admin.site.register(DolarBlue)
admin.site.register(Source)
admin.site.register(Currency)
admin.site.register(CurrencyValue)