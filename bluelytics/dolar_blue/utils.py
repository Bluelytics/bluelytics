import json, pytz,decimal

arg = pytz.timezone("America/Argentina/Buenos_Aires")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)