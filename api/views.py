from django.http import JsonResponse

from api.v1.serializers import MaterialSerializer, Material, CourseSerializer, Course, QuestionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def query(object, search_param):
  if search_param == None:
    return 1, object
  search_params = search_param[0].split(' ')
  count = 0
  obj_title = object.title.lower()
  obj_comment = object.comment.lower()
  course_code = object.course.code.lower()
  course_title = object.course.title.lower()
  department_name = object.department_name.lower()
  
  for search_param in search_params:
    if search_param.lower() in obj_title:
      count += 1
    if search_param.lower() in obj_comment:
      count += 1
    if search_param.lower() in course_code:
      count += 1
    if search_param.lower() in course_title:
      count += 1
    if search_param.lower() in department_name:
      count += 1
  return count, object



@api_view(['GET'])
def get_materials(request):
  GET = dict(request.GET)
  search_param = GET.get('search', None)
  course_level = GET.get('course__level', None)
  course = GET.get('course__code', None)
  if course:
    materials = Material.objects.select_related('course').filter(course__code=course[0])
  else:
    materials = Material.objects.select_related('course').all()
  materials = (query(obj, search_param) for obj in materials)
  materials = filter(lambda x: x[0]>=1, materials)
  materials = map(lambda x: x[1], sorted(materials, key=lambda x: x[0], reverse=True))
  serialize_materials = MaterialSerializer(materials, many=True, context={'request': request})
  return Response(serialize_materials.data)
  
@api_view(['GET'])
def get_courses(request):
  GET = request.GET
  department_id = (GET.get('department__id'))
  level = int(GET.get('level'))
  courses = Course.objects.filter(department__id=department_id, level=level)
  serialize_courses = CourseSerializer(courses, many=True, context={'request': request})
  return Response(serialize_courses.data)

@api_view(['GET'])
def get_quizze(request):
  GET = request.GET
  code = (GET.get('code'))
  course = Course.objects.get(code=code)
  serialize_course = QuestionSerializer(course.objectives.all(), many=True, context={'request': request})
  return Response(serialize_course.data)