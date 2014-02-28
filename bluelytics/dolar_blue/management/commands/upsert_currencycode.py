from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import Currency
from django.utils import timezone

from decimal import Decimal
import sys, datetime

class Command(BaseCommand):
    args = 'code description'
    help = 'Adds or updates the specified currency'

    def handle(self, *args, **options):
        
        if len(args) < 2:
            raise CommandError('Incorrect arguments')
        
        try:
            curr_inst = Currency.objects.get(code=args[0])
        except Exception:
            curr_inst = Currency(code=args[0])

        try:
            curr_inst.name = " ".join(args[1:])
            curr_inst.save()
            self.stdout.write('Successfully saved currency')
        except Exception:
            self.stdout.write('Error saving currency')
            print "Error:", sys.exc_info()[0]
            raise
