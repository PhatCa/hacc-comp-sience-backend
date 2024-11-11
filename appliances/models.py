from django.db import models

# Create your models here.


class Appliance(models.Model):
    name = models.CharField(max_length=200)
    power_usage = models.FloatField()
    is_on = models.BooleanField(default=False)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            self.save()
    
    def turn_off(self):
        if self.is_on:
            self.is_on = False
            self.save()