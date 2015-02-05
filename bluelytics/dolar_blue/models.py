from django.db import models
import json, pytz

from dolar_blue.utils import DecimalEncoder, arg

class Source(models.Model):
    source = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)

    def __json__(self):
      return source

    def __unicode__(self):
      return self.source


class DolarBlue(models.Model):
    value_buy = models.DecimalField(decimal_places=4, max_digits=10)
    value_sell = models.DecimalField(decimal_places=4, max_digits=10)
    source = models.ForeignKey('source', to_field="source")
    date = models.DateTimeField()

    def _get_value_avg(self):
       "Returns the average price"
       if self.value_buy == None or self.value_sell == None:
         return None
       return (self.value_buy + self.value_sell) / 2
    value_avg = property(_get_value_avg)


    def json(self):
      return json.dumps({
        'date': self.date.astimezone(arg).strftime("%d/%m/%Y %H:%M:%S"),
        'value_buy': self.value_buy,
        'value_sell': self.value_sell,
        'value_avg': self.value_avg}
        ,cls=DecimalEncoder)

    def __unicode__(self):
      return self.source.source


class Currency(models.Model):
  code = models.CharField(max_length=3, unique=True)
  name = models.CharField(max_length=150)

  def __unicode__(self):
    return self.code

class CurrencyValue(models.Model):
  curr = models.ForeignKey(Currency)
  date = models.DateTimeField()
  value = models.DecimalField(decimal_places=6, max_digits=14)

  def __unicode__(self):
    return self.curr.code + " " + self.date.strftime("%d/%m/%Y %H:%M:%S")

class BCRA(models.Model):
  date = models.DateField(unique=True)
  Reservas = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  Asistencia = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  BaseMonetaria = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  Circulacion = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  BilletesPublico = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  EfectivoFinanciero = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  DepositosBCRA = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  LEBAC = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  DepositosFinancieras = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  CuentasCorrientes = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  CajasAhorro = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  APlazo = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  OtrosDepositos = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  PrestamosAPrivados = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  TasasInteresEntrePrivadas = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  TasasInteres30Dias = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  BADLAR = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  CambioRef = models.DecimalField(decimal_places=3, max_digits=20, null=True)
  CER = models.DecimalField(decimal_places=3, max_digits=20, null=True)

  def __unicode__(self):
    return self.date.strftime("%d/%m/%Y")
