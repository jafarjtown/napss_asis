from django.urls import include, path
from rest_framework import routers
from api.v1 import views as v1
router = routers.DefaultRouter()

router.register("courses", v1.CourseViewset)
router.register("materials", v1.MaterialViewset)
router.register("past-questions", v1.PassQViewset)


urlpatterns = [
     path('', include(router.urls, namespace='')),
     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
