from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, PasswordInput
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm, PasswordResetForm
#from captcha.fields import ReCaptchaField

from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import CustomUser



class UserRegistrationForm(UserCreationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tuemail@ejemplo.com'})
    )

    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    second_name = forms.CharField(
        label="Segundo nombre",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    father_name = forms.CharField(
        label="Apellido Paterno",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    mother_name = forms.CharField(
        label="Apellido Materno",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )




    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'second_name', 'father_name', 'mother_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.email = self.cleaned_data['email']
        user.second_name = self.cleaned_data.get('second_name')
        user.father_name = self.cleaned_data.get('father_name')
        user.mother_name = self.cleaned_data.get('mother_name')

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

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
    #         'data-theme': 'dark',
    #         'data-size' : 'compact'  # Ejemplo de atributo adicional para reCAPTCHA
    #     })
    # )





