from django.db import models
import json, pytz

from dolar_blue.utils import DecimalEncoder, arg

class DolarBlue(models.Model):
    value_buy = models.DecimalField(decimal_places=6, max_digits=10)
    value_sell = models.DecimalField(decimal_places=6, max_digits=10)
    date = models.DateTimeField('fecha')

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