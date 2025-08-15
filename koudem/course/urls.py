from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create ,name="create"),
    path('courses_list/', views.courses_list ,name="courses_list"),
    path('courses_view/<slug:slug>/', views.courses_view ,name="courses_view"),
    #path('payment_method/<int:alumno_id>/<int:curso_id>/<str:method>', views.payment_methosd, name='payment_methosd'),
    path('payment_method/<int:user_id>/<int:course_id>/', views.payment_method, name='payment_method'),
    path('preinscription_course/<slug:slug>/', views.preinscription_course, name='preinscription_course'),
    path('inscription_user/<int:user_id>/<int:course_id>/<int:option>/', views.inscription_user, name='inscription_user'),
    path('confirmar_pago/<slug:slug>/', views.confirmar_pago, name='confirmar_pago'),
    path('add_car_course/<slug:slug>/', views.add_car_course, name='add_car_course'),
    path('add_car_shop/<slug:slug>/', views.add_car_shop, name='add_car_shop'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('car_shop/', views.car_shop, name='car_shop'),

]



