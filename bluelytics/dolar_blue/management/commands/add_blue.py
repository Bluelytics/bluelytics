from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import DolarBlue
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    args = 'valor_compra valor_venta'
    help = 'Adds the specified dollar value to the database'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Incorrect arguments')

        try:
            db = DolarBlue(date=timezone.now(), value_buy = Decimal(args[0]), value_sell=Decimal(args[1]))
            db.save()
            self.stdout.write('Successfully saved new dollar values')
        except Exception:
            self.stdout.write('Error saving new dollar values')