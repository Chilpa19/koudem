#from django.forms import ModelForm
from .models import *
from django import forms

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name","category","level","cost","status",
                  "start_date","start_date_time","end_date","image", 
                  "limit", "availability","days"
                ]
        widgets = {
            'days': forms.CheckboxSelectMultiple(
                choices=Course.DAY_CHOICES
            )
        }
    status= forms.ChoiceField(
        label="Selecciona un estatus",
        choices=[("Open","Open"),("Close","Close"),("In progress","In progress")])
    