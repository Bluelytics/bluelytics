from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dolar_blue.models import DolarBlue, Source
from dolar_blue.calculations import maxSources, convDolar

from dolar_blue.utils import median, buy_multiplier

from decimal import Decimal
import sys, subprocess, os, datetime
import requests



def send_request_twitter(msg):
    from buffer_apikeys import buffer_accesstoken

    payload = {
        'access_token': buffer_accesstoken,
        'text': msg,
        'profile_ids[]': '532affdc1d36e0037832ea01',
        'shorten': 'false',
        'top': 'true',
        'now': 'true',
        'media[photo]': 'http://api.bluelytics.com.ar/social_img/twitter.png',
        'media[thumbnail]': 'http://api.bluelytics.com.ar/social_img/twitter.png'
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
        'now': 'true',
        'media[photo]': 'http://api.bluelytics.com.ar/social_img/facebook.png',
        'media[thumbnail]': 'http://api.bluelytics.com.ar/social_img/facebook.png'
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
            'value_sell': median(map(lambda x: x['value_sell'], only_blue))
        }
        avg_blue['value_buy'] = avg_blue['value_sell'] * buy_multiplier
        avg_blue['value_avg'] = (avg_blue['value_buy'] + avg_blue['value_sell']) / 2
        oficial = only_oficial[0]

        self.dolar = {}
        self.dolar['blue'] = convert_presentacion(avg_blue)
        self.dolar['oficial'] = convert_presentacion(oficial)
        self.dolar['ahorro'] = convert_presentacion(multiply(oficial, Decimal('1.20')))
        self.dolar['turismo'] = convert_presentacion(multiply(oficial, Decimal('1.35')))

        self.avg_blue = avg_blue


    def twitter_update(self):
        send_request_twitter("Blue a %s, visita http://www.bluelytics.com.ar !" % self.dolar['blue']['sell'])

    def facebook_update(self):
        send_request_facebook("Blue a %s\n\nVisita http://www.bluelytics.com.ar para la ultima informacion!" % self.dolar['blue']['sell'])

    def generate_img(self):
        PATH_SCRIPT_IMG = '/home/sicarul/blueimg/'

        subprocess.call([os.path.join(PATH_SCRIPT_IMG, 'gen_image.sh'),
            str(self.dolar['blue']['buy']),
            str(self.dolar['blue']['sell']),
            str(self.dolar['oficial']['buy']),
            str(self.dolar['oficial']['sell']),
            str(self.dolar['ahorro']['buy']),
            str(self.dolar['ahorro']['sell']),
            str(self.dolar['turismo']['buy']),
            str(self.dolar['turismo']['sell']),
        ])

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')

        try:
            self.prepare_data()
            self.generate_img()
            social_network = args[0]
            if(social_network == 'twitter' or social_network == 'all'):
                self.twitter_update()
            if(social_network == 'facebook' or social_network == 'all'):
                self.facebook_update()


        except Exception:
            self.stdout.write('Error updating social network')
            print "Error:", sys.exc_info()[0]
            raise
