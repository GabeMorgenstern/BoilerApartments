from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# This is the only table, it serves to represent apartments added to the application
class Apartment(models.Model):
    company_name = models.CharField(max_length=200)
    complex_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    lease_start_date = models.DateTimeField()
    lease_length = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)

    class Meta: # indexed on price, lease date, and lease length for faster filter and ordering
        indexes = [models.Index(fields=['price']), models.Index(fields=['lease_start_date']), models.Index(fields=['lease_length']),]
        
    def __str__(self):
        return self.complex_name
