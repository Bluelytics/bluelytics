from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import DolarBlue, Source
from django.utils import timezone

from decimal import Decimal
import sys, datetime, json
from dolar_blue.utils import DecimalEncoder, arg


def last_prices_each_day():
    return DolarBlue.objects.raw('\
    select db.*\
    from dolar_blue_dolarblue db\
    inner join\
    (select source_id, max(date) as date, date(date) as datepart\
      from dolar_blue_dolarblue\
      group by source_id, date(date)\
    ) dbj\
    on db.source_id = dbj.source_id and db.date = dbj.date\
    where db.date > now()::date - 730\
    order by db.date;\
    ')

def api_mini_dolar(d):
    return {
    'date': d.date.astimezone(arg).isoformat(),
    'value': d.value_avg
    }

class Command(BaseCommand):
    args = 'valor_compra valor_venta'
    help = 'Adds the specified dollar value to the database'


    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')
        print args
        try:
            output = {}

            items = last_prices_each_day()
            for src in Source.objects.all():
                toadd = []
                for item in items:
                  if item.source == src:
                    toadd.append(item)
                output[src.description] = map(api_mini_dolar, toadd)

            with open(args[0], 'w') as j:
                json.dump(output, j, cls=DecimalEncoder)

            self.stdout.write('Successfully exported graph data')
        except Exception:
            self.stdout.write('Error exporting graph data')
            print "Error:", sys.exc_info()[0]
            raise
