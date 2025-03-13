from material.models import Material, Course, PastQuestion, Department
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.v1.serializers import MaterialSerializer, CourseSerializer, PastQSerializer, DepartmentSerializer, BlogPage, BlogListPageSerializer, BlogDetailPageSerializer, DepartmentCoursesSerializer
#from rest_framework_word_filter import FullWordSearchFilter 
#from url_filter.integrations.drf import DjangoFilterBackend



class BlogPageViewset(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListPageSerializer  # For listing
        return BlogDetailPageSerializer  # For details
        
        
class DepartmentViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows Department to be viewed or edited.
    """
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #filter_fields = ['course','title', "upload_on"]
    #word_fields = ('title','comment','course__code', 'course__title')
    #filter_backends = (FullWordSearchFilter,DjangoFilterBackend )

    def get_serializer_class(self):
        if self.action == 'list':
            return DepartmentSerializer  # For listing
        return DepartmentCoursesSerializer  # For details

class MaterialViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows materials to be viewed or edited.
    """
    
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_fields = ['course','title', "upload_on"]
    #word_fields = ('title','comment','course__code', 'course__title')
    #filter_backends = (DjangoFilterBackend,)
    
    
class CourseViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    
    #word_fields = ('title','info','code')
    #filter_fields = ["department", "level"]
    #filter_backends = (FullWordSearchFilter,DjangoFilterBackend )
    
class PassQViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows pass questions to be viewed or edited.
    """
    queryset = PastQuestion.objects.all()
    serializer_class = PastQSerializer
    #permission_classes = [permissions.AllowAny]
    #filter_fields = ["course"]
    #filter_backends = (FullWordSearchFilter,DjangoFilterBackend )
    
