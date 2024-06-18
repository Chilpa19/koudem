from django.contrib import admin
from django.urls import path,include

from . import views


urlpatterns = [
    path('login/', views.custom_login,name="custom_login"),
    path('logout/', views.exit ,name="exit"),
    path("register/",views.register, name="register")
]
