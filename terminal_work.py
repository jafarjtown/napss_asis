from material.models import Course, Department
import json
def upload_department():
  with open('json files/departments.json') as js:
    objs = json.load(js)
    for obj in objs:
      Department.objects.get_or_create(name=obj['name'], slogan=obj['slogan'])
      print('###')
      
def upload_courses():
  with open('json files/courses.json') as js:
    objs = json.load(js)
    for obj in objs:
      if Department.objects.filter(name=obj['department']).exists():
        d = Department.objects.filter(name=obj['department'])[0]
      else:
        d = Department.objects.create(name=obj['department'])
      for c in obj['courses']:
        print(c)
        if Course.objects.filter(code=c['code']).exists():
          continue
        Course.objects.create(code=c['code'], title=c['title'], level=c['level'], department=d)
      # course.department=d
        # course.save()
      print('###')