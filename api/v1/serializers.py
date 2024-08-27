from rest_framework import serializers
from material.models import Material, Course, PastQuestion

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["url", "course", "title", "comment","upload_on","file", "code", "flag_url", "department_name"]
        
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields= ["url", "code", "title", "info", "materials"]

class PastQSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastQuestion
        fields = ["year", "url", "course", "pq"]
