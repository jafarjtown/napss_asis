# app/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import mimetypes, os

# Create your models here.

def materials_directory_path(instance, filename):
    code = "-".join(instance.code.split(" "))
    name = "-".join(instance.department.name.split(" "))
    return f"materials/{name}/{code}/{filename}"

def material_name(instance):
    return instance.file.name
    


class Material(models.Model):
    title= models.CharField(max_length=200, default="")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="materials")
    file = models.FileField(upload_to=materials_directory_path)
    comment= models.TextField()
    upload_on = models.DateTimeField(auto_now_add=True)
    
    @property
    def type(self):
        
        mime_type, _ = mimetypes.guess_type(self.file.name)
        if mime_type:
            main_type, sub_type = mime_type.split('/')
            return main_type
        return "files"
    @property
    def code(self):
        return self.course.code
    
    @property
    def department(self):
        return self.course.department
        
    @property
    def department_name(self):
        return self.department.name
    
    @property
    def flag_url(self):
        return reverse("material:flag_material", kwargs={"mid":self.id})
    @property 
    def size(self):
        file_size = self.file.size
        if file_size < 1024:
            return f"{file_size} bytes"
        elif 1024 <= file_size < 1024 * 1024:
            return f"{file_size // 1024} KB"
        else:
            return f"{file_size // (1024 * 1024)} MB"

    def __str__(self):
        return self.title
        
        
    def delete(self, *args, **kwargs):
        if self.file:
            path_file = self.file.path
            print(path_file)
            if os.path.exist(path_file):
                pring("deleting")
                os.remove(path_file)
                print("finish deleting")
        return self.delete(*args, **kwargs)



class Request(models.Model):
    body = models.TextField()
    topic = models.CharField(max_length=50)
    priority = models.IntegerField(default=0)
    type = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

class Department(models.Model):
    name = models.CharField(max_length=50)
    slogan = models.TextField()

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    level = models.CharField(max_length=3)
    lectures = models.ManyToManyField('LectureHour', blank=True)
    
    def __str__(self):
      return f'{self.level} {self.department}'
    def lecture_days(self):
      days = Day.objects.all()
      return days
    
    def lecture_times(self):
      times = Time.objects.all()
      return times
    
    def lectures_day(self):
      results = []
      days = self.lecture_days()
      times = self.lecture_times()
      context = {}
      for time in times:
        for day in days:
          if day not in context:
            context[day] = []
          lecture = self.lectures.filter(hour=time, day=day).first()
          context[day].append({'time':time, 'class':lecture})
      return context.items()
      
class LectureHour(models.Model):
  course = models.ForeignKey('Course', on_delete=models.CASCADE)
  day = models.ForeignKey('Day', on_delete=models.CASCADE)
  hour = models.ForeignKey('Time', on_delete=models.CASCADE)
  venue = models.CharField(max_length=20, default='NFY')
  
  def __str__(self):
    return f'{self.course} at {self.hour}'

class Time(models.Model):
  time = models.CharField(max_length=20)
  index = models.PositiveIntegerField(default=0)
  class Meta:
    ordering = ['index']
  
  def __str__(self):
    return self.time
  def format(self, formater='/'):
    return f'{self.time}'

class Day(models.Model):
  name = models.CharField(max_length=10)
  
  def __str__(self):
    return self.name
    
class Course(models.Model):
    code = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    info = models.TextField()
    outline = models.FileField(upload_to="courses/outlines/", null=True, blank=True)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    level = models.IntegerField(default=100)
    
    def comments_set(self):
        return self.comments.all().order_by("-posted_on")[:10]
    def __str__(self):
        return self.code

class BlogBase(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    
    class Meta:
        abstract = True
    
class Blog(BlogBase):
    pass

class Comment(BlogBase):
    blog = models.ForeignKey("Blog", on_delete = models.CASCADE)
    reply = models.ManyToManyField("Comment", blank=True)

class CourseComment(models.Model):
    user = models.CharField(max_length=20)
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    posted_on = models.DateTimeField(auto_now_add=True)
    
    
    

class PastQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="pass_questions")
    pq = models.FileField(upload_to="pq")
    year = models.DateField(auto_now=False)
