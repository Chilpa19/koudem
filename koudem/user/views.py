from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import UserForm, UserRegistrationForm, EmailAuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import logout, login, get_user_model
from django.urls import reverse

# Mensajes
from django.contrib import messages
# Encryption
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.db.models.query_utils import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import datetime
from django.conf import settings

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + 
            str(user.is_active)
        )
    
    def check_token(self, user, token, expiration_seconds=1800):
        try:
            ts_b36, _ = token.split("-")
            ts = int(ts_b36, 36)
        except ValueError:
            return False
        
        expiry_date = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(seconds=expiration_seconds)
        
        if datetime.datetime.now() > expiry_date:
            return False
        
        return super().check_token(user, token)

account_activation_token = AccountActivationTokenGenerator()

def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
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

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user"
    message = render_to_string("users/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })  
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user} please go to your email {to_email}")
    else:
        messages.error(request, 'Problem sending email')

@login_required
def exit(request):
    logout(request)
    return redirect('dashboard')

def register(request):
    if request.user.is_authenticated:
        return redirect("portal")
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('username'))
            return render(request, "./users/verificationRegister.html", {})
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, "./registration/registration.html", {"form": form})

def custom_login(request, course_id=None):
    if request.user.is_authenticated:
        return redirect("portal")
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and course_id is None:
                login(request, user)
                return redirect('portal')
            else:
                login(request, user)
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

    return render(request, "users/login.html", {"form": form})

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully")
            return redirect('portal')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form})

def password_reset(request):
    if request.user.is_authenticated:
        return redirect("portal")
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(username=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("users/template_reset_password.html", {
                    'user': associated_user.username,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })  
                email = EmailMessage(subject, message, to=[associated_user.username])
                if email.send():
                    messages.success(request, "Password reset email sent successfully")
                else:
                    messages.error(request, "Problem sending email")
            return render(request, "users/sending_confirmation.html", {'user': associated_user.username})
    else:
        form = PasswordResetForm()
    return render(request, "users/password_reset.html", {"form": form})

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set")
                return redirect('/user/login/')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        form = SetPasswordForm(user)
        return render(request, "users/password_reset_confirm.html", {'form': form})
    else:
        messages.error(request, "Link expired or invalid")
    
    return redirect('/user/login/')

def getUser(request, id):
    User = get_user_model()
    user = User.objects.get(pk=id)
    # Deberías retornar una respuesta aquí, por ejemplo:
    return HttpResponse(f"User: {user.username}")

@login_required(login_url='/user/login/')    
def view_profile(request):
    return render(request, 'users/perfil_usuario.html', {'user_profile': request.user})
