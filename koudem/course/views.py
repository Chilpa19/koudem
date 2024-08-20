from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .form import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,get_user_model


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

        # Obtener el curso con el ID dado
    course = get_object_or_404(Course, id=course_id)
    
    # Pasar el curso al contexto
    context = {
        'course': course,
    }
   
    return render(request, "./course/viewCourse.html",context)


# @login_required
# def inscribir_alumno(request, alumno_id, curso_id):
#     alumno = get_object_or_404(User, id=alumno_id)
#     curso = get_object_or_404(Course, id=curso_id)
    
#     # Crear la inscripción si no existe
#     inscripcion, created = Inscription.objects.get_or_create(alumno=alumno, curso=curso)
    
#     # Redirigir a alguna página después de la inscripción
#     return redirect('nombre_de_tu_vista')



@login_required
def payment_method(request, user_id, course_id):
    print("Payment")
    course = get_object_or_404(Course, id=course_id)
    #user = modelsU.objects.get(id=user_id)
    # User = get_user_model()
    # user = User.objects.get(pk=user_id)
    user = get_object_or_404(User, id=user_id)
    #userP = get_object_or_404(modelsU, id=user_id)
    print("Payment 2", user_id,course_id,user.first_name)
    # Pasar el curso al contexto
    context = {
        'course': course,
        'user': user
    }
   
    return render(request, "./course/choicePaymentCourse.html",context)






