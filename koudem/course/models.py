from django.db import models
from datetime import date
from django.contrib.auth.models import User
# from user.models import User



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
    
class Inscription(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,null=False,blank=False, default="Postulado")
    # Puedes añadir otros campos relevantes, como la calificación, estado de la inscripción, etc.
    
    class Meta:
        unique_together = ('alumno', 'course')  # Para asegurar que no haya inscripciones duplicadas

    def __str__(self):
        return f"{self.alumno} inscrito en {self.course}"
    
    










