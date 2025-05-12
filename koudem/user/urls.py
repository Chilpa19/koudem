from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('login/', views.custom_login,name="custom_login"),
    path('login/<int:course_id>/',views.custom_login,name="custom_login"),
    path('logout/', views.exit ,name="exit"),
    path("register/",views.register, name="register"),
    path("activate/<uidb64>/<token>",views.activate, name="activate"),
    path("password_change", views.password_change, name="password_chang"),
    path("password_reset", views.password_reset, name="password_resete"),
    path("reset/<uidb64>/<token>", views.passwordResetConfirm, name="password_resete_confirm"),

]+ staticfiles_urlpatterns()
