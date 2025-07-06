from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .form import UserForm, UserRegistrationForm, EmailAuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import logout,login,get_user_model
from django.urls import reverse

#Mensajes
from django.contrib import messages
#Encryption
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.db.models.query_utils import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import datetime
from django.conf import settings

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + 
            six.text_type(user.is_active)
        )
    
    def check_token(self, user, token, expiration_seconds=1800):  # Cambiado a segundos
        try:
            ts_b36, _ = token.split("-")
            ts = int(ts_b36, 36)
        except ValueError:
            return False
        
        # Calcula la fecha de expiración (30 segundos por defecto)
        expiry_date = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(seconds=expiration_seconds)
        
        if datetime.datetime.now() > expiry_date:
            return False
        
        return super().check_token(user, token)

account_activation_token = AccountActivationTokenGenerator()


def activate(request,uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active= True
        user.save()
        messages.success(request, "Thanks now you can login")
        
        return redirect('custom_login')
    else:
        try:
            ts_b36, _ = token.split("-")
            ts = int(ts_b36, 36)
            expiry_date = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(seconds=30)
            if datetime.datetime.now() > expiry_date:
                messages.error(request, "El enlace de activación ha expirado (válido solo por 30 segundos).")
            else:
                messages.error(request, "El enlace de activación no es válido.")
        except:
            messages.error(request, "El enlace de activación no es válido.")
    
    return redirect('portal')



def activateEmail(request,user,to_email):
    mail_subject = "Activate your user"
    message = render_to_string("users/template_activate_account.html",{
                            'user': user.username,
                            'domain': get_current_site(request).domain,
                            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                            'token' : account_activation_token.make_token(user),
                            "protocol" : 'https' if request.is_secure() else 'http'
    })  
    email = EmailMessage(mail_subject,message, to=[to_email])
    if email.send():
        messages.success(request, f" Dear {user} plis go to your email {to_email}")
    else:
        message.errors(request,f'Problem sending email')


@login_required
def exit(request):
    logout(request)
    return redirect('dashboard')


def register(request):
    if request.user.is_authenticated:
        return redirect("portal")
    print("Registration")
    if request.user.is_authenticated:
        return redirect('portal/')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('username'))
            #messages.success(request,"Ejemplo de succes")
            #return redirect('custom_login')
            return render(request=request, template_name="./users/verificationRegister.html",context={})
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    else:
        form = UserRegistrationForm()
    return render(request=request, template_name="./registration/registration.html",context={"form":form})


def custom_login(request,course_id=None):
    print("Login custom")
    if request.user.is_authenticated:
        return redirect("portal")
    if request.method == 'POST':
        print("Post")
        form = EmailAuthenticationForm(request.POST)

        if form.is_valid():
            user = form.get_user()
            print(user,"user")
            if user is not None and course_id==None:
                print("Authenticated")
                login(request,user)
                return redirect('portal')
            else:
                login(request,user)
                return redirect(reverse('courses_view', args=[course_id]))
        else:
            print("mo valid")
            print(len(list(form.errors)))
            print(form.errors)
            for key,error in list(form.errors.items()):
                if key=='captcha' and error[0]=="This field is required.":
                    print("Error de CAPTCHA")
                    messages.error(request,"Selecciona Captcha")
                    continue
                print("key",key,"ERRER",error)
                messages.error(request,error)
        
            
    else:
        form = EmailAuthenticationForm()

    return render(request,"users/login.html",{"form":form})


def password_change(request):
    print("Password_change")
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password cool")
            return redirect('portal')
        else:
            for error in list(form.error.values()):
                messages.error(request,error)
    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form':form})

def password_reset(request):
    print("Gets")
    if request.user.is_authenticated:
        return redirect("portal")
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            print(user_email,"userrrr")
            associated_user = get_user_model().objects.filter(Q(username=user_email)).first()
            print(associated_user,"Associated")
            print(associated_user.pk,"pk")
            print(associated_user.__dict__,"dicttt")
            if associated_user:
                subject = "Passwors Reset request"
                message = render_to_string("users/template_reset_password.html",{
                            'user': associated_user.username,
                            'domain': get_current_site(request).domain,
                            'uid' : urlsafe_base64_encode(force_bytes(associated_user.pk)),
                            'token' : account_activation_token.make_token(associated_user),
                            "protocol" : 'https' if request.is_secure() else 'http'
                            })  
                email = EmailMessage(subject, message, to=[associated_user.username])

                if email.send():
                    print("Se envia correo")
                    messages.success(request,
                    """
                        Se envia con exito el correo
                    """)
                else:

                    messages.error(request, "Problem sending")
                    print(messages.error(request, "Problem sending"))
            return render(request,"users/sending_confirmation.html",{'user':associated_user.username})
     
        for key,error in list(form.errors.items()):
            if key=='captcha' and error[0]=="This field is required.":
                print("Error de CAPTCHA")
                messages.error(request,"Selecciona Captcha")
                continue
            
            messages.error(request,error)

    form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html", context={"form":form})


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user,"user")
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        print("Nice?")
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                print("Se cambio exitosamente")
                messages.success(request,"Your password has been set")
            else:
                print("Error")
                for error in list(form.error.values()):
                    messages.error(request,error)
                    print(error)
            return redirect('/user/login/')
        form=SetPasswordForm(user)
        return render(request,"users/password_reset_confirm.html",{'form':form})
    else:
        messages.error(request, "linked expired")
        print("<Link expiró")

    messages.error(request, "SOmethis went wrong")
    return redirect('/user/login/')

def getUser(request,id):
    User = get_user_model()
    user = User.objects.get(pk=id)


@login_required(login_url='/user/login/')    
def view_profile(request):
    user = request.user
    return render(request, 'users/perfil_usuario.html', {'user_profile': request.user})
