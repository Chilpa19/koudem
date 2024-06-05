from django.db import models
from datetime import date


class Course(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    category = models.CharField(max_length=50, null=False,blank=False)
    level =models.CharField(max_length=50, null=False,blank=False)
    cost =models.CharField(max_length=10,default="0.0",null=False,blank=False)
    status = models.CharField(max_length=50,null=False)
    start_date=models.DateField(default=date.today())
    end_date=models.DateField(default=date.today())
    image = models.ImageField(upload_to='images/',default="",null=True)

    def __str__(self):
        return self.name
    









