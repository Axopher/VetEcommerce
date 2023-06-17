from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200,unique=True)
    email = models.EmailField(max_length=200,unique=True)   
    # phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username