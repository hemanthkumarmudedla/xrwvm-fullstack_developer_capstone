# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPE_CHOICES = [
        ('SED', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAG', 'Wagon'),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=3, choices=CAR_TYPE_CHOICES)
    year = models.IntegerField()
    
    def __str__(self):
        return f"{self.make.name} {self.name}"

