from django.db import models

class CSVModel(models.Model):
    url = models.URLField(max_length=300)