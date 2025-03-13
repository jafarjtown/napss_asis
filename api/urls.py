from django.urls import include, path
from rest_framework import routers
from api.v1 import views as v1
from .views import get_materials, get_courses, get_quizze
router = routers.DefaultRouter()

router.register("courses", v1.CourseViewset)
router.register("blogs", v1.BlogPageViewset)
router.register("materials", v1.MaterialViewset)
router.register("department", v1.DepartmentViewset)
router.register("past-questions", v1.PassQViewset)


urlpatterns = [
     path('', include(router.urls, namespace='')),
     path('beta/materials/', get_materials),
     path('beta/courses/', get_courses),
     path('beta/quizze/', get_quizze),
     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
