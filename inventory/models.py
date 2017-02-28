from django.db import models


class snack(models.Model):
    name = models.TextField()
    optional = models.BooleanField()
    purchaseLocations = models.TextField(default="None Listed")
    purchaseCount = models.IntegerField(default=0)
    lastPurchaseDate = models.TextField(null=True, default="Never Purchased")
    votes = models.IntegerField(default=0)
