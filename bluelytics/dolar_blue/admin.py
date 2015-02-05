from django.contrib import admin

from dolar_blue.models import DolarBlue, Source, Currency, CurrencyValue, BCRA

admin.site.register(DolarBlue)
admin.site.register(Source)
admin.site.register(Currency)
admin.site.register(CurrencyValue)
admin.site.register(BCRA)
