from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# from .form import UserForm
from django.contrib.auth.decorators import login_required


def portal(request):
    username=request.POST['username']
    context={"username":username}
    return render(request,'menu/portal.html',context)

@login_required
def mision(required):
    return HttpResponse("Soy Msiions")

