from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import DolarBlue, Source
from django.utils import timezone

from decimal import Decimal
import sys, datetime

class Command(BaseCommand):
    args = 'valor_compra valor_venta'
    help = 'Adds the specified dollar value to the database'

    def handle(self, *args, **options):
        if len(args) < 3:
            raise CommandError('Incorrect arguments')
        print args
        try:
            source_inst = Source.objects.get(source=args[2])
            now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
            if len(args) == 4:
                now = datetime.datetime.strptime('%s 13' % args[3], '%d-%m-%Y %H')

            if Decimal(args[0]) < 1 or Decimal(args[1]) < 1:
                self.stdout.write('Value too low')
                return
            db = DolarBlue(date=now, value_buy = Decimal(args[0]), value_sell=Decimal(args[1]), source=source_inst)

            db.save()
            self.stdout.write('Successfully saved new dollar values')
        except Exception:
            self.stdout.write('Error saving new dollar values')
            print "Error:", sys.exc_info()[0]
            raise
