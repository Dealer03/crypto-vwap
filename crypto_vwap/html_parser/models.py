from django.db import models
from django.contrib.auth.models import User


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
    # volume = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.side}"
