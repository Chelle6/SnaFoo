from django.db import models

from django.db import models

class snack(models.Model):
	name = models.TextField()  # string
	optional = models.BooleanField()  # boolean
	purchaseLocations = models.TextField(default="None Listed")  # string
	purchaseCount = models.IntegerField(default=0)  # integer
	lastPurchaseDate = models.TextField(null=True, default="Never Purchased")  # string 
	votes = models.IntegerField(default=0)