from rest_framework import serializers
from app.models import Material, Course, PastQuestion

class MaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Material
        fields = ["url", "course", "title", "comment","upload_on","file", "code", "flag_url", "department_name"]
        
        
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields= ["url", "code", "title", "info", "materials"]

class PastQSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PastQuestion
        fields = ["year", "url", "course", "pq"]
