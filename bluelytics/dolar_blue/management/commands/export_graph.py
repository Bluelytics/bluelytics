from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import DolarBlue, Source
from django.utils import timezone

from decimal import Decimal
import sys, datetime, json
from dolar_blue.utils import DecimalEncoder, arg


def last_prices_each_day():
    return DolarBlue.objects.raw('\
    select\
    0 as id, a.date, a.source_id, b.value_buy, b.value_sell from\
    (\
    select\
      date(db.date), src.source as source_id\
    from\
      dolar_blue_dolarblue db\
      inner join dolar_blue_source src\
      on 1=1\
      group by date(db.date), src.source\
    ) a\
    inner join\
    (\
      select\
      max(db.value_buy) as value_buy, max(db.value_sell) as value_sell, db.source_id, date(db.date) as date\
      from\
      dolar_blue_dolarblue db \
      group by db.source_id, date(db.date)\
      order by date(db.date)\
    ) b\
    on a.date = b.date and a.source_id = b.source_id\
    ;\
    ')

def api_mini_dolar(d):
    return {
    'date': d.date.isoformat(),
    'value': d.value_sell
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
