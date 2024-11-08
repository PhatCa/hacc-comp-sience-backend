from django.db import models

# Create your models here.


class Appliance(models.Model):
    name = models.CharField(max_length=200)
    power_usage = models.FloatField()
    is_on = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    