from django.db import models

class MenuItem(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.SmallIntegerField()
