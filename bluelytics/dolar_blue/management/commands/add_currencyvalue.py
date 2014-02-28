from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import Currency, CurrencyValue
from django.utils import timezone

from decimal import Decimal
import sys, datetime

class Command(BaseCommand):
    args = 'code value'
    help = 'Adds a new value for the specified currency'

    def handle(self, *args, **options):
        
        if len(args) != 2:
            raise CommandError('Incorrect arguments')
        
        try:
            curr_inst = Currency.objects.get(code=args[0])
            now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)

            curr_val = CurrencyValue(date=now, curr=curr_inst, value=Decimal(args[1]))
            curr_val.save()

            self.stdout.write('Successfully saved currency value')
        except Exception:
            self.stdout.write('Error saving currency value')
            print "Error:", sys.exc_info()[0]
            raise
