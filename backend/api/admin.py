from django.contrib import admin
from .models import Schedule, Student, Enrollment, Course, Availability

# Register your models here.
admin.site.register(Schedule)
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Course)
admin.site.register(Availability)
