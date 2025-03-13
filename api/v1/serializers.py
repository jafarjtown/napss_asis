from rest_framework import serializers
from material.models import Material, Course, PastQuestion, Department
from cbt.models import Question, Option
from blog.models import BlogPage, Document, Tag


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["file"]

    def to_representation(self, instance):
        return instance.file.url  # Return only the value, not a dict

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["value"]

    def to_representation(self, instance):
        return instance.value # Return only the value, not a dict

class BlogListPageSerializer(serializers.ModelSerializer):
    cover_image = DocumentSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = BlogPage
        fields = ["id", "title", "cover_image", "tags", "created_at"]

class BlogDetailPageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author_email = serializers.SerializerMethodField()
    cover_image = DocumentSerializer()
    class Meta:
        model = BlogPage
        fields = ["id", "author_email", "title", "cover_image", "tags", "created_at", "content"]

    def get_author_email(self, obj):
        return obj.author.email  # Fetch only the email from the User model

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["url", "course", "title", "comment","upload_on","file", "code", "flag_url", "department_name", "download_url"]
        
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields= ["url", "code", "title", "info", "materials"]

class PastQSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastQuestion
        fields = ["year", "url", "course", "pq"]
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["value"]

    def to_representation(self, instance):
        return instance.value  # Return only the value, not a dict


class QuestionSerializer(serializers.ModelSerializer):
    a = OptionSerializer()
    b = OptionSerializer()
    c = OptionSerializer()
    d = OptionSerializer()
    correct_answer = OptionSerializer()
    class Meta:
        model = Question
        fields = ["question", "a", "b", "c", 'd', 'correct_answer']

class DepartmentCoursesSerializer(serializers.ModelSerializer):
    course_set = CourseSerializer(many=True)
    class Meta:
        model = Department
        fields = "__all__"
        
    def get_courses(self, obj):
      return obj.course_set.all()
        
