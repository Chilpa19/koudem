#from django.forms import ModelForm
from .models import *
from django import forms

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name","category","level","cost","status",
                  "start_date","end_date","image"
                ]
    cost= forms.ChoiceField(
        label="Selecciona un precio",
        choices=[("200","200"),("300","300")])
    