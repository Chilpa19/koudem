from django.contrib import admin
from .models import Course, Inscription


class CourseAdmin(admin.ModelAdmin):
    list_display=("name","category")
    # search_fields=("name","email")
    # list_filter = ("name",)
    # date_hierarchy="birthday"

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("alumno", "course", "date_inscription", "status", "progress", "grade")
    list_filter = ("status", "course")

admin.site.register(Course,CourseAdmin)
admin.site.register(Inscription, InscriptionAdmin)


