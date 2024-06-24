from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, PasswordInput
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm, PasswordResetForm
#from captcha.fields import ReCaptchaField

from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from . import models

class UserForm(ModelForm):
    class Meta:
        model=models.User
        fields=["username"]


class UserRegistrationForm(UserCreationForm):
    #email = forms.EmailField(help_text="A valid email :))", required=True)
    username = forms.EmailField(label="Email pero es username",help_text="Helped")

    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','username','password1','password2']

    def save(self, commit=True):
        user =super(UserRegistrationForm,self).save(commit=False)
        #user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user    
    

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255,required=True)
    password = forms.CharField(label= 'Password',widget=PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
            'data-theme': 'dark',
            'data-size' : 'compact'  # Ejemplo de atributo adicional para reCAPTCHA
        })
    )

    def __init__(self, *args,**kwards):
        self.user_cache = None
        super().__init__(*args,**kwards)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate( username=email,password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Credenciales invalidas")
            
            
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache

class SetPasswordForm(SetPasswordForm):

    class Meta:
        model = get_user_model()
        fields = ['new_password1','new_password2']


class PasswordResetForm(PasswordResetForm):
    
        
    def __init__(self, *args,**kwards):
        super(PasswordResetForm,self).__init__(*args,**kwards)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
            'data-theme': 'dark',
            'data-size' : 'compact'  # Ejemplo de atributo adicional para reCAPTCHA
        })
    )





