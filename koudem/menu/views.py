
from django.http import HttpResponse
from django.shortcuts import render
# from .form import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,get_user_model
# En views.py u otro archivo donde necesites usar Course
from course.models import Course
from django.utils import timezone



def portal(request):
    if request.method == 'POST':
        username = request.POST['username']
    else:
        username = ''

    # now = timezone.now()

    # # Cursos futuros -> "Open"
    # Course.objects.filter(
    #     start_date_time__gt=now
    # ).update(status="Open")

    # # Cursos que están ocurriendo -> "In progress"
    # Course.objects.filter(
    #     start_date_time__lte=now,
    #     end_date_time__gt=now
    # ).update(status="In progress")

    # # Cursos terminados -> "Close"
    # Course.objects.filter(
    #     end_date_time__lte=now
    # ).update(status="Close")

    courses = Course.objects.all()

    context = {
        "username": username,
        "courses": courses
    }
    
    return render(request, 'menu/portal.html', context)


def mision(request):
    return HttpResponse("Soy Msiions")

def vision(request):
    return HttpResponse("Soy vision")

def dashboard(request):
    return render(request,"menu/dashboard.html",{})


