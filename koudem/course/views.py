from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .form import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,get_user_model
from datetime import datetime
from django.db.models import Q

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
    # Obtener todos los cursos con posibles filtros
    courses = Course.objects.all()
    
    # Obtener parámetros de filtrado del GET request para todos los cursos
    category_filter = request.GET.get('category')
    level_filter = request.GET.get('level')
    search_query = request.GET.get('search')
    
    # Aplicar filtros si existen para todos los cursos
    if category_filter:
        courses = courses.filter(category=category_filter)
    if level_filter:
        courses = courses.filter(level=level_filter)
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Cursos enrolados con filtros independientes
    user = request.user
    inscriptions = Inscription.objects.filter(alumno=user)
    cursos_user = [i.course for i in inscriptions]
    
    # Obtener parámetros de filtrado específicos para "Mis Cursos"
    my_category_filter = request.GET.get('my_category')
    my_level_filter = request.GET.get('my_level')
    my_search_query = request.GET.get('my_search')
    
    # Aplicar filtros a "Mis Cursos" si existen
    if my_category_filter:
        cursos_user = [course for course in cursos_user if course.category == my_category_filter]
    if my_level_filter:
        cursos_user = [course for course in cursos_user if course.level == my_level_filter]
    if my_search_query:
        search_lower = my_search_query.lower()
        cursos_user = [course for course in cursos_user 
                      if search_lower in course.name.lower() or 
                      search_lower in course.description.lower()]
    
    # Obtener opciones únicas para los selectores de filtro
    all_categories = Course.objects.values_list('category', flat=True).distinct()
    all_levels = Course.objects.values_list('level', flat=True).distinct()
    
    # Obtener categorías y niveles específicos de "Mis Cursos" para los filtros
    user_categories = list(set([course.category for course in cursos_user]))
    user_levels = list(set([course.level for course in cursos_user]))
    
    context = {
        "courses": courses,
        "courses_user": cursos_user,
        "categories": all_categories,
        "levels": all_levels,
        "user_categories": user_categories,
        "user_levels": user_levels,
    }
    
    response = render(request, "./course/displayCourse.html", context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response



   
def courses_view(request, slug):
    print("===========View course==========")
    user=request.user
    statusInscri=""
    course = get_object_or_404(Course, slug=slug)

    # if course.status == "Open" and course.start_date <= date.today():
    #     course.status = "In progress"
    #     course.save()
    course_id = course.id
    print("Course_id",course_id)

    # Obtener el curso con el ID dado
    if request.user.is_authenticated:
        
        inscription_exists = Inscription.objects.filter(alumno=user, course=course_id)

        try:
            statusInscri=inscription_exists[0].status
        except IndexError:
            statusInscri=None
    # Pasar el curso al contexto
    context = {
        'course': course,
        "exits" : statusInscri
    }

    response = render(request, "./course/viewCourse.html", context)

    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
   
    return response


@login_required
def inscription_user(request, user_id, course_id, option):
    #user = get_object_or_404(User, id=user_id)
    curso = get_object_or_404(Course, id= course_id)

    #User = get_user_model()
    alumno = User.objects.get(pk=user_id)

    alumno=request.user

    inscription, created = Inscription.objects.get_or_create( course=curso,alumno=alumno,date_inscription=datetime.now())
    # inscription.date_inscription = date.today()
    # inscription.save()
    print("Inscripcion",inscription.__dict__)


    if option == 1:
        url_whatsapp = "https://wa.me/525522495140?text=Hola,%20estoy%20interesado%20en%20tu%20producto"
        return HttpResponseRedirect(url_whatsapp)
    else:
        print("Opcion 2")
        url_whatsapp = "https://wa.me/525522495140?text=Hola,%20estoy%20interesado%20en%20tu%20producto"
        return HttpResponseRedirect(url_whatsapp)

    
    # Redirigir a alguna página después de la inscripción
    
@login_required
def preinscription_course(request, slug):
    print("Preinscription")

    course = get_object_or_404(Course, slug=slug)
    alumno = request.user  # ✅ Usa el usuario autenticado correctamente

    # Buscar si ya existe inscripción
    inscription = Inscription.objects.filter(course=course, alumno=alumno).first()

    if not inscription:
        inscription = Inscription.objects.create(
            course=course,
            alumno=alumno,
            date_inscription=datetime.now()
        )
        print("Inscripción creada")
    else:
        print("La inscripción ya existe")

    context = {
        'course': course,
        'user': alumno
    }
    return render(request, "./course/preinscriptionCourse.html", context)



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



@login_required
def confirmar_pago(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_id = course.id
    user_id=request.user.id
    cursoP = get_object_or_404(Course, id=course_id)
    alumnoP = get_object_or_404(User, id=user_id)
    inscription = Inscription.objects.filter(course=cursoP, alumno=alumnoP).first()
    
    if inscription:
        inscription.status = "Inscrito"
        inscription.save()
        print("Inscripción actualizada a 'Inscrito'")
    else:
        print("No se encontró inscripción para actualizar")

    return redirect('courses_view', slug=slug)



