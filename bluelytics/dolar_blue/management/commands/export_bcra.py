from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import BCRA
from django.utils import timezone

from decimal import Decimal
import sys, datetime, json
from dolar_blue.utils import DecimalEncoder, arg


def api_bcra(d):
    return {
    'date': d.date.isoformat(),
    'Reservas': d.Reservas,
    'Asistencia': d.Asistencia,
    'BaseMonetaria': d.BaseMonetaria,
    'Circulacion': d.Circulacion,
    'BilletesPublico': d.BilletesPublico,
    'EfectivoFinanciero': d.EfectivoFinanciero,
    'DepositosBCRA': d.DepositosBCRA,
    'LEBAC': d.LEBAC,
    'DepositosFinancieras': d.DepositosFinancieras,
    'CuentasCorrientes': d.CuentasCorrientes,
    'CajasAhorro': d.CajasAhorro,
    'APlazo': d.APlazo,
    'OtrosDepositos': d.OtrosDepositos,
    'PrestamosAPrivados': d.PrestamosAPrivados,
    'TasasInteresEntrePrivadas': d.TasasInteresEntrePrivadas,
    'TasasInteres30Dias': d.TasasInteres30Dias,
    'BADLAR': d.BADLAR,
    'CambioRef': d.CambioRef,
    'CER': d.CER
    }

class Command(BaseCommand):
    args = 'filename'
    help = 'Exports the specified bcra to a file'


    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')
        print args
        try:

            items = BCRA.objects.all()
            output = map(api_bcra, items)

            with open(args[0], 'w') as j:
                json.dump(output, j, cls=DecimalEncoder)

            self.stdout.write('Successfully exported bcra data')
        except Exception:
            self.stdout.write('Error exporting bcra data')
            print "Error:", sys.exc_info()[0]
            raise
