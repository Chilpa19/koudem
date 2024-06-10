from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display=("name","category")
    # search_fields=("name","email")
    # list_filter = ("name",)
    # date_hierarchy="birthday"

admin.site.register(Course,CourseAdmin)


