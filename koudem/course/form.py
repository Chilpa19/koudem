#from django.forms import ModelForm
from .models import *
from django import forms

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name","category","level","cost","status",
                  "start_date","start_date_time","end_date","image","days"
                ]
        widgets = {
            'days': forms.CheckboxSelectMultiple(
                choices=Course.DAY_CHOICES
            )
        }
    cost= forms.ChoiceField(
        label="Selecciona un precio",
        choices=[("200","200"),("300","300")])
    