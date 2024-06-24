from django.shortcuts import redirect, render
from django.http import HttpResponse
from .form import *
from django.contrib.auth.decorators import login_required


def create(request):
    
    if request.method=='GET':
        print("Get curso create")
        form=CreateCourseForm()
        context={"form":form}
        return render(request,"./course/createCourse.html",context)
    else:
        form = CreateCourseForm(request.POST, request.FILES)
        print(form)
        print("Curso ?")
        if form.is_valid():
            print("is valid")
            form.save()
            return redirect('courses_list')
        
        return HttpResponse("Curso NO Saved :c")


@login_required    
def courses_list(request):
    courses = Course.objects.all()
    print(courses)
    for i in courses:
        print(i.image)
    context={"courses":courses}
   
    return render(request, "./course/displayCourse.html",context)



@login_required    
def courses_view(request, course_id):
    # courses = Course.objects.all()
    # print(courses)
    # for i in courses:
    #     print(i.image)
    context={"id":course_id}
   
    return render(request, "./course/viewCourse.html",context)





