# models.py

from django.db import models

from accounts.models import CustomUser

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    percent_change_24h = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio')

    def __str__(self):
        return self.name
