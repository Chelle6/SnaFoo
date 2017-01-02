from django.db import models

class snack(models.Model):
	name = models.TextField()  # string
	optional = models.BooleanField()  # boolean
	purchaseLocations = models.TextField()  # string
	purchaseCount = models.IntegerField()  # integer
	lastPurchaseDate = models.TextField()  # string