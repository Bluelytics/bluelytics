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
    source = models.CharField(max_length=30)

    def _get_value_avg(self):
       "Returns the average price"
       return (self.value_buy + self.value_sell) / 2
    value_avg = property(_get_value_avg)


    def json(self):
      arg = pytz.timezone("America/Argentina/Buenos_Aires")
      json.dumps({'x': decimal.Decimal('5.5')}, cls=DecimalEncoder)
      return json.dumps({
        'date': self.date.astimezone(arg).strftime("%d/%m/%Y %H:%M:%S"),
        'value_buy': self.value_buy,
        'value_sell': self.value_sell,
        'value_avg': self.value_avg}
        ,cls=DecimalEncoder)
>>>>>>> d9bd5e4568709a6aa0b8629c7a95527c35de7bbf
