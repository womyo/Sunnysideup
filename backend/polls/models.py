from django.db import models

class Rise(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    standard_time = models.FloatField()
    image_link = models.URLField()

class Set(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    standard_time = models.FloatField()
    image_link = models.URLField()
