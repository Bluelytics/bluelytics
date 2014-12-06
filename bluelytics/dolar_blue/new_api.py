from dolar_blue.utils import json_response
from dolar_blue.calculations import maxSources, convDolar


@json_response
def latest(request):
    max_sources = map(convDolar, maxSources())
    sources_blue = filter(lambda x: x['source'] != 'oficial',max_sources)
    source_oficial = filter(lambda x: x['source'] == 'oficial',max_sources)[0]


    last_date = None

    blue_buy = sum(map(lambda x: x['value_buy'], sources_blue))/len(sources_blue)
    blue_avg = sum(map(lambda x: x['value_avg'], sources_blue))/len(sources_blue)
    blue_sell = sum(map(lambda x: x['value_sell'], sources_blue))/len(sources_blue)

    response = {}
    response['oficial'] = {'value_buy': source_oficial['value_buy'], 'value_avg': source_oficial['value_avg'], 'value_sell': source_oficial['value_sell']}
    response['blue'] = {'value_buy': blue_buy,  'value_avg': blue_avg, 'value_sell': blue_sell}
    response['last_update'] = max(map(lambda x:x['date'], max_sources))

    return response
