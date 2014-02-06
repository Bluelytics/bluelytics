from django.db import models

class DolarBlue(models.Model):
    value_buy = models.DecimalField(decimal_places=6, max_digits=10)
    value_sell = models.DecimalField(decimal_places=6, max_digits=10)
    date = models.DateTimeField('fecha')