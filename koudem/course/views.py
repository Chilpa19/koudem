from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
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


@login_required(login_url='/user/login/')    
def courses_list(request):
    #Todos los cursos
    courses = Course.objects.all()
    print(courses)
    for i in courses:
        print(i.image)
   
   #Cursos enrolados
    user=request.user
    inscriptions = Inscription.objects.filter(alumno=user)

    print("Incripciones de usuario",inscriptions)

    cursos_user = [i.course for i in inscriptions]

    # for i in inscriptions:
    #     print("Un curso",i.course,type(i.course))
    #     print(i.__dict__)



    context={"courses":courses,
             "courses_user":cursos_user}
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


@login_required
def inscription_user(request, user_id, course_id, option):
    #user = get_object_or_404(User, id=user_id)
    curso = get_object_or_404(Course, id= course_id)

    #User = get_user_model()
    alumno = User.objects.get(pk=user_id)

    alumno=request.user

    inscription, created = Inscription.objects.get_or_create( course=curso,alumno=alumno)

    if option == 1:
        url_whatsapp = "https://wa.me/525522495140?text=Hola,%20estoy%20interesado%20en%20tu%20producto"
        return HttpResponseRedirect(url_whatsapp)
    else:
        print("Opcion 2")
        url_whatsapp = "https://wa.me/525522495140?text=Hola,%20estoy%20interesado%20en%20tu%20producto"
        return HttpResponseRedirect(url_whatsapp)

    
    # Redirigir a alguna página después de la inscripción
    



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


def payment_course(user_id, course_id):
    usuario = get_object_or_404(User, id=user_id)
    curso = get_object_or_404(Course, id=course_id)
    inscripcion = get_object_or_404(Inscription, usuario=usuario, curso=curso)
    
    # Modifica el atributo
    inscripcion.estado = 'Completado'  # Ejemplo de actualización
    
    # Guarda los cambios
    inscripcion.save()







