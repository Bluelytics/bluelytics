from django.db import models
import json, decimal, pytz

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class DolarBlue(models.Model):
    value_buy = models.DecimalField(decimal_places=6, max_digits=10)
    value_sell = models.DecimalField(decimal_places=6, max_digits=10)
    date = models.DateTimeField('fecha')

    def json(self):
      arg = pytz.timezone("America/Argentina/Buenos_Aires")
      json.dumps({'x': decimal.Decimal('5.5')}, cls=DecimalEncoder)
      return json.dumps({
        'date': self.date.astimezone(arg).strftime("%d/%m/%Y %H:%M:%S"),
        'value_buy': self.value_buy,
        'value_sell': self.value_sell}
        ,cls=DecimalEncoder)