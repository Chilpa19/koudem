from django.db import models



class User(models.Model):
    username = models.CharField(max_length=50,null=False,blank=False)
    name = models.CharField(max_length=50, null=False,blank=False)
    last_ape =models.CharField(max_length=50, null=False,blank=False)
    last_mat =models.CharField(max_length=50, null=False,blank=False)
    email = models.EmailField(max_length=50,null=False)


