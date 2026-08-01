from django.db import models

# Create your models here.
from django.db import models
class Package(models.Model):
 name = models.CharField(max_length=100)
 price = models.DecimalField(max_digits=10, decimal_places=2)
 duration = models.IntegerField(help_text="Duration in days")
 description = models.TextField()

created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.name