
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
    hoy = timezone.now().date()

    # Course.objects.filter(
    #     start_date__lt=hoy,
    #     status="In progress"
    #     ).update(status="Close")

    courses = Course.objects.filter(start_date__gte=hoy)

    #courses = Course.objects.all()

    print("Courses", courses)



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


