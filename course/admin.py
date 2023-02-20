from django.contrib import admin
from course.models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(GeneralEducation)
admin.site.register(GenedSatisfaction)
admin.site.register(Semester)
admin.site.register(Grade)
admin.site.register(UserInput)
