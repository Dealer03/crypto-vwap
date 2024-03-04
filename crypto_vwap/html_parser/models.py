from decimal import Decimal
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
        # Get all transactions for the specified asset
        transactions = cls.objects.filter(asset=asset)

        # Calculate the weighted sum of average prices and total filled quantity
        weighted_sum = sum(float(transaction.average) *
                           float(transaction.filled) for transaction in transactions)
        total_filled_quantity = transactions.aggregate(total_filled=Sum('filled'))[
            'total_filled'] or Decimal('0')

        # Calculate the weighted average price
        if total_filled_quantity != Decimal('0'):
            weighted_average_price = weighted_sum / total_filled_quantity
        else:
            weighted_average_price = Decimal('0')

        weighted_average_price = "{:.2f}".format(weighted_average_price)

        return weighted_average_price

    @classmethod
    def current_holdings(cls, asset):
        total_filled = cls.objects.filter(
            asset=asset).aggregate(Sum('filled'))['filled__sum']
        return total_filled or 0

    @classmethod
    def get_current_holdings(cls, asset):
        # Filtering buy transactions where realized profit is 0.0
        buys = cls.objects.filter(asset=asset, realized_profit=0.0).aggregate(
            total_buy_filled=Sum('filled'))['total_buy_filled'] or 0

        # Filtering sell transactions where realized profit is not 0.0
        sells = cls.objects.filter(asset=asset).exclude(realized_profit=0.0).aggregate(
            total_sell_filled=Sum('filled'))['total_sell_filled'] or 0

        # Calculating current holdings
        current_holdings = buys - sells

        current_holdings = Decimal('{:.2f}'.format(current_holdings))

        return current_holdings


def __str__(self):
    return f"{self.date} - {self.side}"
