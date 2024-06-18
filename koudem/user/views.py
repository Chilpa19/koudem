from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render
#Mensajes
from django.contrib import messages

from .form import UserForm, UserRegistrationForm
from django.contrib.auth import logout

def login(request):
    if request.method=='GET':
        form=UserForm()
        context={"form":form}
        return render(request,"./users/login.html",context)
    else:
        username=request.POST['username']
        context={"username":username}
        return render(request,'./test.html',context)
    

def exit(request):
    logout(request)
    return redirect('dashboard')

def register(request):
    print("Registration")
    if request.user.is_authenticated:
        return redirect('dashboard/')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            #login(request,user)
            messages.success(request,"Ejemplo de succes")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    else:
        form = UserRegistrationForm()
    return render(request=request, template_name="./registration/registration.html",context={"form":form})

    



