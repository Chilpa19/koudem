from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create ,name="create"),
    path('courses_list/', views.courses_list ,name="courses_list"),
    path('courses_view/<int:course_id>/', views.courses_view ,name="courses_view"),
    #path('payment_method/<int:alumno_id>/<int:curso_id>/<str:method>', views.payment_methosd, name='payment_methosd'),
    path('payment_method/<int:user_id>/<int:course_id>/', views.payment_method, name='payment_method'),
    path('inscription_user/<int:user_id>/<int:course_id>/<int:option>/', views.inscription_user, name='inscription_user'),
]

