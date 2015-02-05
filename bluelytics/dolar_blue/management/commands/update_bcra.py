from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import BCRA
from django.utils import timezone

from decimal import Decimal
import sys, datetime, csv

class Command(BaseCommand):
    args = 'csv_folder'
    help = 'Updates bcra values'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')
        folder = args[0]
        print "Buscando archivos csv en %s" % folder
        fields = ['CER','CambioRef','BADLAR','TasasInteres30Dias','TasasInteresEntrePrivadas','PrestamosAPrivados','OtrosDepositos','APlazo','CajasAhorro','CuentasCorrientes','DepositosFinancieras','LEBAC','DepositosBCRA','EfectivoFinanciero','BilletesPublico','Circulacion','BaseMonetaria','Asistencia','Reservas']

        for x in fields:
          path = "%s%s.csv" % (folder,x)
          print "procesando %s..." % path

          with open(path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
              date = datetime.datetime.strptime(row['date'], "%Y-%m-%d").date()
              value = row['x']
              
              try:
                obj = BCRA.objects.get(date=date)
              except BCRA.DoesNotExist:
                obj = BCRA(date=date)

              setattr(obj, x, value)
              obj.save()
