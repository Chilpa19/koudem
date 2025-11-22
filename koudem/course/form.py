#from django.forms import ModelForm
from .models import *
from django import forms

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name","category","level","cost","status",
                  "start_date","end_date","image", 
                  "limit", "availability","days","start_time","end_time"
                ]
        widgets = {
            'days': forms.CheckboxSelectMultiple(
                choices=Course.DAY_CHOICES
            )
        }
    status= forms.ChoiceField(
        label="Selecciona un estatus",
        choices=[("Open","Open"),("Close","Close"),("In progress","In progress")])
    