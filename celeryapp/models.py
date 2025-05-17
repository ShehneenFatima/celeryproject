from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at_pst = models.DateTimeField(default=timezone.now)
    created_at_utc = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

# Create your models here.
