from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dolar_blue.models import DolarBlue, Source
from dolar_blue.calculations import maxSources, convDolar

from decimal import Decimal
import sys, datetime
import requests



def send_request_twitter(msg):
    from buffer_apikeys import buffer_accesstoken
    
    payload = {
        'access_token': buffer_accesstoken,
        'text': msg,
        'profile_ids[]': '532affdc1d36e0037832ea01',
        'shorten': 'false',
        'top': 'true',
        'now': 'true'
    }
    r = requests.post("https://api.bufferapp.com/1/updates/create.json", data=payload)
    

def send_request_facebook(msg):
    from buffer_apikeys import buffer_accesstoken
    
    payload = {
        'access_token': buffer_accesstoken,
        'text': msg,
        'profile_ids[]': '532afee31d36e0eb7732ea02',
        'shorten': 'false',
        'top': 'true',
        'now': 'true'
    }
    r = requests.post("https://api.bufferapp.com/1/updates/create.json", data=payload)
    

def convert_presentacion(values):
    return {
        'buy': "%.2f" % values['value_buy'],
        'avg': "%.2f" % values['value_avg'],
        'sell': "%.2f" % values['value_sell']
    }

def multiply(values, m):
    return {
        'value_buy': m * values['value_buy'],
        'value_avg': m * values['value_avg'],
        'value_sell': m * values['value_sell']
    }

class Command(BaseCommand):
    args = 'social_network'
    help = 'Sends an update to each social network'

    

    def prepare_data(self):
        last_data = map(convDolar, maxSources())
        only_blue = filter(lambda x: x['source'] != 'oficial', last_data)
        only_oficial = filter(lambda x: x['source'] == 'oficial', last_data)
        avg_blue = {
            'value_buy': reduce(lambda x,y: x+y['value_buy'], only_blue, 0) / len(only_blue),
            'value_sell': reduce(lambda x,y: x+y['value_sell'], only_blue, 0) / len(only_blue)
        }
        avg_blue['value_avg'] = (avg_blue['value_buy'] + avg_blue['value_sell']) / 2
        oficial = only_oficial[0]

        self.dolar = {}
        self.dolar['blue'] = convert_presentacion(avg_blue)
        self.dolar['oficial'] = convert_presentacion(oficial)
        self.dolar['ahorro'] = convert_presentacion(multiply(oficial, Decimal('1.20')))
        self.dolar['turismo'] = convert_presentacion(multiply(oficial, Decimal('1.35')))

        self.avg_blue = avg_blue


    def twitter_update(self):     
        send_request_twitter("[Blue] Venta a %s, Compra a %s, Intermedio a %s - Visita el sitio para + info! http://goo.gl/DUj1XN" \
        % (self.dolar['blue']['sell'], self.dolar['blue']['buy'], self.dolar['blue']['avg']) )

        send_request_twitter("[Oficial] Venta a %s, Compra a %s, Intermedio a %s - Visita el sitio para + info! http://goo.gl/DUj1XN" \
        % (self.dolar['oficial']['sell'], self.dolar['oficial']['buy'], self.dolar['oficial']['avg']) )

        send_request_twitter("[Oficial+20%%/Ahorro] Venta a %s, Compra a %s, Intermedio a %s - Visita el sitio para + info! http://goo.gl/DUj1XN" \
        % (self.dolar['ahorro']['sell'], self.dolar['ahorro']['buy'], self.dolar['ahorro']['avg']) )

        send_request_twitter("[Oficial+35%%/Turismo] Venta a %s, Compra a %s, Intermedio a %s - Visita el sitio para + info! http://goo.gl/DUj1XN" \
        % (self.dolar['turismo']['sell'], self.dolar['turismo']['buy'], self.dolar['turismo']['avg']) )


    def facebook_update(self):
        send_request_facebook("\
    Te informamos los valores del dia!\
[Blue] Venta a %s, Compra a %s, Intermedio a %s\n\
[Oficial] Venta a %s, Compra a %s, Intermedio a %s\n\
[Oficial+20%%/Ahorro] Venta a %s, Compra a %s, Intermedio a %s\n\
[Oficial+35%%/Turismo] Venta a %s, Compra a %s, Intermedio a %s\n\
Para mas informacion y actualizaciones periodicas visita nuestro sitio web!\n\
http://goo.gl/DUj1XN\
" % \
        ( \
        self.dolar['blue']['sell'], self.dolar['blue']['buy'], self.dolar['blue']['avg'],\
        self.dolar['oficial']['sell'], self.dolar['oficial']['buy'], self.dolar['oficial']['avg'],\
        self.dolar['ahorro']['sell'], self.dolar['ahorro']['buy'], self.dolar['ahorro']['avg'],\
        self.dolar['turismo']['sell'], self.dolar['turismo']['buy'], self.dolar['turismo']['avg'],\
        ))

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')
        
        try:
            self.prepare_data()
            social_network = args[0]
            if(social_network == 'twitter' or social_network == 'all'):
                self.twitter_update()
            if(social_network == 'facebook' or social_network == 'all'):
                self.facebook_update()
            

        except Exception:
            self.stdout.write('Error saving new dollar values')
            print "Error:", sys.exc_info()[0]
            raise
