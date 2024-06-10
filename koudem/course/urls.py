from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create ,name="create"),
    path('courses_list/', views.courses_list ,name="courses_list"),
    path('courses_view/<int:course_id>/', views.courses_view ,name="courses_view"),
]

