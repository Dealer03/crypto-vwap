from django.db import models


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

    def __str__(self):
        return f"{self.date} - {self.side}"
