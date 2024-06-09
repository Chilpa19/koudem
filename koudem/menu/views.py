
from django.http import HttpResponse
from django.shortcuts import render
# from .form import UserForm
from django.contrib.auth.decorators import login_required


def portal(request):
    if request.method=='POST':
        username=request.POST['username']

    context={"username":" "}
    return render(request,'menu/portal.html',context)


def mision(request):
    return HttpResponse("Soy Msiions")

def vision(request):
    return HttpResponse("Soy vision")

def dashboard(request):
    return render(request,"menu/dashboard.html",{})


