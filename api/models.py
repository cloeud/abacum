from django.db import models

class DataModel(models.Model):
    date = models.DateField()
    account = models.IntegerField()
    amount = models.FloatField()
    
    class Meta:
        db_table = "transactions"