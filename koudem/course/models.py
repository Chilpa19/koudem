from django.db import models
from django.conf import settings
from datetime import date
from payments.models import OrderDetail



from django.utils.text import slugify
from django.utils import timezone
import datetime
from django.contrib.postgres.fields import ArrayField



class Course(models.Model):
    DAY_CHOICES=[
        ('LUN','LUNES'),
        ('MAR','MARTES'),
        ('MIE','MIERCOLES'),
        ('JUE','JUEVES'),
        ('VIE','VIERNES'),
        ('SAB','SABADO'),
    ]
    name = models.CharField(max_length=50,null=False,blank=False)#
    category = models.CharField(max_length=50, null=False,blank=False)#
    level =models.CharField(max_length=50, null=False,blank=False)#
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50,null=False)#
    image = models.ImageField(upload_to='images/',default="",null=True)#
    description = models.CharField(max_length=300,null=False,blank=False,default="description")
    slug = models.SlugField(unique=True, blank=True)
    start_date_time = models.DateTimeField(blank=False, default=timezone.now)#
    end_date_time = models.DateTimeField(blank=False, default=timezone.now)#
    limit=models.IntegerField(blank=False,null=False,default=15)
    availability=models.IntegerField(blank=False, null=False, default=15)
    days=ArrayField(models.CharField(
        max_length=3,
        choices=DAY_CHOICES
    ),verbose_name="Días",blank=True,default=list)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
class Inscription(models.Model):
    alumno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_detail=models.ForeignKey(OrderDetail,  on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


    date_inscription = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50,null=False,blank=False, default="Postulado")
    progress = models.FloatField(default=0.0)  # Para almacenar el progreso del estudiante.
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('alumno', 'course')  # Para asegurar que no haya inscripciones duplicadas

    def __str__(self):
        return f"{self.alumno} inscrito en {self.course}"
    
    










