from django.urls import path
from . import views

app_name = 'material'
urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('materials/', views.material_list, name='material_list'),   
    path('past-questions/', views.past_questions, name='pqs'),   
    path('search/', views.search_materials, name='search'),
    path("api/courses/<int:dep>/<int:lev>/", views.courses_api, name="courses-api"),
    path("timetables/", views.timetable_view, name="timetables"),
    path("timetables/<int:id>/", views.timetable, name="timetable"),
    path("courses/", views.courses, name="course"),
    path("courses/<int:cid>/outline/", views.upload_outline, name="upload_outline"),
    path("courses/<int:id>/bulkdownload/", views.bulk_download_materials, name="bulk_download_materials"),
    path("courses/<int:cid>/flag-issue/", views.flag_course, name="flag_course"),
    path("materials/<int:mid>/flag-issue/", views.flag_material, name="flag_material"),
    path('download/material/<int:material_id>/', views.download_material, name='download_material'),
    
  ]