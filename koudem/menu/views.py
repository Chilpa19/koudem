
from django.http import HttpResponse
from django.shortcuts import render
# from .form import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,get_user_model
# En views.py u otro archivo donde necesites usar Course
from course.models import Course
from django.utils import timezone



def portal(request):

    if request.method=='POST':
        username=request.POST['username']

    courses = Course.objects.all()

    Course.objects.filter(
        status="Open",
        start_date_time__lte=timezone.now()
    ).update(status="In progress")

    context={"username":" ",
             "courses": courses}
    
    return render(request,'menu/portal.html',context)


def mision(request):
    return HttpResponse("Soy Msiions")

def vision(request):
    return HttpResponse("Soy vision")

def dashboard(request):
    return render(request,"menu/dashboard.html",{})


