from django.db import models
import json, pytz

from dolar_blue.utils import DecimalEncoder, arg

class Source(models.Model):
    source = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)

    def __json__(self):
      return source

class DolarBlue(models.Model):
    value_buy = models.DecimalField(decimal_places=4, max_digits=10)
    value_sell = models.DecimalField(decimal_places=4, max_digits=10)
    source = models.ForeignKey('source', to_field="source")
    date = models.DateTimeField()

    def _get_value_avg(self):
       "Returns the average price"
       return (self.value_buy + self.value_sell) / 2
    value_avg = property(_get_value_avg)


    def json(self):
      return json.dumps({
        'date': self.date.astimezone(arg).strftime("%d/%m/%Y %H:%M:%S"),
        'value_buy': self.value_buy,
        'value_sell': self.value_sell,
        'value_avg': self.value_avg}
        ,cls=DecimalEncoder)