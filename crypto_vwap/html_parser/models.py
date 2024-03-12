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
    quantity = models.FloatField()
    fee = models.FloatField()
    realized_profit = models.FloatField()
    volume = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def weighted_average_price(cls, asset):
        # Get all transactions for the specified asset
        transactions = cls.objects.filter(asset=asset)

        # Calculate the weighted sum of average prices and total quantity
        weighted_sum = sum(float(transaction.average) *
                           float(transaction.quantity) for transaction in transactions)
        total_quantity_quantity = transactions.aggregate(total_quantity=Sum('quantity'))[
            'total_quantity'] or Decimal('0')

        # Calculate the weighted average price
        if total_quantity_quantity != Decimal('0'):
            weighted_average_price = weighted_sum / total_quantity_quantity
        else:
            weighted_average_price = Decimal('0')

        weighted_average_price = "{:.2f}".format(weighted_average_price)

        return weighted_average_price

    @classmethod
    def current_holdings(cls, asset):
        total_quantity = cls.objects.filter(
            asset=asset).aggregate(Sum('quantity'))['quantity__sum']
        return total_quantity or 0

    @classmethod
    def get_current_holdings(cls, asset):
        # Filtering buy transactions where realized profit is 0.0
        buys = cls.objects.filter(asset=asset, realized_profit=0.0).aggregate(
            total_buy_quantity=Sum('quantity'))['total_buy_quantity'] or 0

        # Filtering sell transactions where realized profit is not 0.0
        sells = cls.objects.filter(asset=asset).exclude(realized_profit=0.0).aggregate(
            total_sell_quantity=Sum('quantity'))['total_sell_quantity'] or 0

        # Calculating current holdings
        current_holdings = buys - sells

        current_holdings = Decimal('{:.2f}'.format(current_holdings))

        return current_holdings


def __str__(self):
    return f"{self.date} - {self.side}"
