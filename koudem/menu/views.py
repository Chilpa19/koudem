from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# from .form import UserForm


def portal(request):
    username=request.POST['username']
    context={"username":username}
    return render(request,'menu/portal.html',context)

