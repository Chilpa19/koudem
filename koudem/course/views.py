from django.shortcuts import render
from django.http import HttpResponse
from .form import *

def create(request):
    
    if request.method=='GET':
        form=CreateCourseForm()
        context={"form":form}
        return render(request,"./course/createCourse.html",context)
    else:
        form = CreateCourseForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return render(request,"./course/displayCourse.html")
        return HttpResponse("Curso NO Saved :c")
    
def courses_list(request):
    courses = Course.objects.all()
    print(courses)
    for i in courses:
        print(i.image)
    context={"courses":courses}
   
    return render(request, "./course/displayCourse.html",context)





