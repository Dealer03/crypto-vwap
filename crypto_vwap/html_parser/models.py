from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Transaction(models.Model):
    date = models.DateField()
    side = models.CharField(max_length=50)
    sub_wallet = models.CharField(max_length=50)
    type = models.CharField(max_length=15)
    asset = models.CharField(max_length=15)
    average = models.FloatField()
    filled = models.FloatField()
    fees = models.FloatField()
    realized_profit = models.FloatField()
    volume = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


@classmethod
def weighted_average_price(cls, asset):
    transactions = cls.objects.filter(asset=asset)
    total_volume = transactions.aggregate(Sum('volume'))['volume__sum']
    if total_volume:
        weighted_sum = sum(transaction.average *
                           transaction.volume for transaction in transactions)
        return weighted_sum / total_volume
    return 0


@classmethod
def current_holdings(cls, asset):
    total_filled = cls.objects.filter(
        asset=asset).aggregate(Sum('filled'))['filled__sum']
    return total_filled or 0


def __str__(self):
    return f"{self.date} - {self.side}"
