from dolar_blue.utils import json_response, median
from dolar_blue.calculations import maxSources, convDolar
from dolar_blue.models import Currency, CurrencyValue
from decimal import *

@json_response
def latest(request):
    max_sources = map(convDolar, maxSources())
    sources_blue = filter(lambda x: x['source'] != 'oficial',max_sources)
    source_oficial = filter(lambda x: x['source'] == 'oficial',max_sources)[0]

    euro = Currency.objects.filter(code__exact='EUR')[0]
    eurovalue = CurrencyValue.objects.filter(curr__exact=euro.id).last()
    euro_avg = eurovalue.value
    euro_buy = euro_avg * Decimal(1.03)
    euro_sell = euro_avg * Decimal(0.97)
    last_date = None

    blue_buy = Decimal(median(map(lambda x: x['value_buy'], sources_blue)))
    blue_avg = Decimal(median(map(lambda x: x['value_avg'], sources_blue)))
    blue_sell = Decimal(median(map(lambda x: x['value_sell'], sources_blue)))

    response = {}
    response['oficial'] = {'value_buy': source_oficial['value_buy'], 'value_avg': source_oficial['value_avg'], 'value_sell': source_oficial['value_sell']}
    response['blue'] = {'value_buy': blue_buy,  'value_avg': blue_avg, 'value_sell': blue_sell}
    response['last_update'] = max(map(lambda x:x['date'], max_sources))
    response['oficial_euro'] = {'value_buy': source_oficial['value_buy']/euro_buy, 'value_avg': source_oficial['value_avg']/euro_avg, 'value_sell': source_oficial['value_sell']/euro_sell}
    response['blue_euro'] = {'value_buy': blue_buy/euro_buy, 'value_avg': blue_avg/euro_avg, 'value_sell': blue_sell/euro_sell}
    return response
