# tu_app/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    second_name = models.CharField(max_length=50, blank=True, null=True)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username
