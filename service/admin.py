from django.contrib import admin
from .models import ServiceType, Service, StudentService, ServicePriority
# Register your models here.



admin.site.register(ServiceType)
admin.site.register(ServicePriority)
admin.site.register(StudentService)
admin.site.register(Service)