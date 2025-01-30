from django.contrib import admin
from .models import Course, Department,Material, PastQuestion, Time, Day, LectureHour, TimeTable, DepartmentRepresentative
# Register your models here.

admin.site.register(Material)
admin.site.register(Course)
admin.site.register(DepartmentRepresentative)
admin.site.register(PastQuestion)
admin.site.register(Department)
admin.site.register(TimeTable)
admin.site.register(Time)
admin.site.register(Day)
admin.site.register(LectureHour)