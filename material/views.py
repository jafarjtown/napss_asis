from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
from django.http import FileResponse, Http404
from django.http import HttpResponse
from django.conf import settings
import os
import zipfile
from io import BytesIO
from .models import Material, Department , Course, TimeTable, CourseComment ,PastQuestion, Day, Time, DepartmentRepresentative
from user_account.models import FlaggedIssue
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import FileComparator
from blog.models import BlogPage, User
# Create your views here.

    
def upload(request):
    context = {
            "departments": Department.objects.all(),
            'levels': [100,200,300,400]
    }
    if request.method == 'POST':
        course = request.POST.get('course')
        comment = request.POST.get('comment')
        department = request.POST.get('department')
        file = request.FILES.get('file')
        title = request.POST.get("title")
        
        course = Course.objects.get(department__id = department, code = course)
        f = FileComparator(file, f"materials/{course.department.name}/{course.code}")
        print(f.get_file_type(file))
        if f.is_same:
            messages.info(request, "Material already exists.")
        else:
           
            try:
                material = Material(course=course, comment=comment, file=file, title=title)
                material.save()
                messages.success(request, "Material added successful")
            except Exception as e:
                print(e)


    return render(request, 'app/upload.html', context)

@login_required
def representative_upload(request, id):
    rep = DepartmentRepresentative.objects.get(id=id, person=request.user)
    context = {
            "departments": [rep.department],
            'levels': [100, 200, 300, 400, 500]
    }
    if request.method == 'POST':
        course = request.POST.get('course')
        comment = request.POST.get('comment')
        department = request.POST.get('department')
        file = request.FILES.get('file')
        title = request.POST.get("title")
        
        course = Course.objects.get(department__id = department, code = course)
        f = FileComparator(file, f"materials/{course.department.name}/{course.code}")
        print(f.get_file_type(file))
        if f.is_same:
            messages.info(request, "Material already exists.")
        else:
           
            try:
                rep.uploaded_materials.create(course=course, comment=comment, file=file, title=title)
                rep.save()
                messages.success(request, "Material added successful")
                #material = Material(course=course, comment=comment, file=file, title=title)
                #material.save()
            except Exception as e:
                print(e)
        if request.htmx:
          return HttpResponse(status=204)


    return render(request, 'app/upload.html', context)

def register_course(request, id):
  rep = DepartmentRepresentative.objects.get(id=id, person=request.user)
  department = rep.department
  context = {
            "departments": [rep.department],
            'levels': [100, 200, 300, 400, 500]
  }
  if request.method == "POST":
    code = request.POST.get("code")
    title = request.POST.get("title")
    info = request.POST.get("info")
    level = request.POST.get("level")
    if department.course_set.filter(code=code.upper()).exists():
      messages.info(request, f'{code} already exist.')
      context['title'] = title
      context['info'] = info
      context['code'] = code
    else:
      department.course_set.create(code=code.upper(), title=title, info=info, level=level)
      messages.success(request, f'{code} added successful.')
      return redirect('material:register_course', rep.id )
  return render(request, 'app/register_course.html', context)
  
def material_list(request):
    departments = Department.objects.all()
    sort = request.GET.get("sort")
    levels = [100, 200, 300, 400]
    
    context = {"departments":departments}
    context["levels"] = levels 
    level = request.GET.get("level")
    department_id = request.GET.get("department")
    course_code = request.GET.get("course")
    if department_id and course_code and department_id != "null" and course_code != "null":
        department = departments.get(id = department_id)
        course = department.course_set.get(code = course_code)
        context["course"] = course
        materials = course.materials.all()
    
        context["materials"] = materials 
        if level:
            context["level"] = int(level)
        context["department"] = department.id
    else:
        context["materials"] = Material.objects.all()
    try:
        context["materials"] = context["materials"].order_by("-upload_on" if sort == "a" else "upload_on")
    except Exception as e:
        print(e)
    return render(request, 'app/list.html', context)


def search_materials(request):
    search_query = request.GET.get('q')

    if search_query:
        materials = Material.objects.select_related("course").filter(course__code__icontains=search_query) | \
                    Material.objects.select_related("course").filter(course__title__icontains=search_query)
    else:
        materials = Material.objects.all()
        search_query = ""

    return render(request, 'app/search.html', {'materials': materials, "q": search_query})


def courses_api(request, dep, lev):
    department = Department.objects.get(id = dep)
    courses = department.course_set.filter(level=lev).values("code", "title")
    return JsonResponse({"data": tuple(courses)})

def timetable_view(request):
    department = request.GET.get('department', False)
    level= request.GET.get('level', False)
    if department and level:
      timetable = TimeTable.objects.get(department__id = int(department), level = int(level))
      return redirect('timetable', timetable.id)
    departments = Department.objects.all()
    sort = request.GET.get("sort")
    levels = [100, 200, 300, 400]
    
    context = {"departments":departments}
    context["levels"] = levels 
    return render(request , "app/timetable_view.html", context)


def timetable(request, id):
    time_table = TimeTable.objects.get(id = id)
    departments = Department.objects.all()
    sort = request.GET.get("sort")
    levels = [100, 200, 300, 400]
    
    context = {"departments":departments}
    context["levels"] = levels 
    context['timetable'] = time_table
    return render(request, "app/timetable.html", context)
    
    
def courses(request):
    context = {"departments": Department.objects.all(), "levels":[100, 200,300,400]}
    if request.GET.get("department") and request.GET.get("course"):
        department = int(request.GET.get("department"))
        level = request.GET.get("level")
        course = request.GET.get("course")
        
        dep = Department.objects.prefetch_related("course_set").get(id = department)
        course = dep.course_set.get(code = course)
        if request.method == "POST":
             #if not request.user.is_authenticated:
             #  return redirect('auth:user_login')
             user = request.POST.get("name")
             comment = request.POST.get("comment")
             if user == "":
                    user = "Anonymous User"
             c = CourseComment(user=user, comment=comment, course=course)
             c.save()
        context["course"] = course
        if level: 
            context["level"] = int(level)
        context["department"] = dep.id
    
    return render(request, "app/course.html", context)
    
    
def upload_outline(request, cid):
    course = Course.objects.get(id = cid)
    if request.method == "POST":
        
        file = request.FILES.get("outline")
        course.outline = file
        course.save()
        messages.success(request, "Course outline uploaded successful")
    return render(request, "app/course_outline.html", {"course":course})
    
    
def flag_course(request, cid):
    course = Course.objects.get(id = cid)
    context = {"course": course}
    if request.method == "POST":
        response = request.POST.get("response")
        email = request.POST.get("email")
        issue = FlaggedIssue(response=response,email=email, issued_object=course)
        issue.save()
        context["flag_id"] = issue.id
        messages.info(request, "Issue is reported successful.")
        
    return render(request, "app/flag_course.html", context)

def flag_material(request, mid):
    material = Material.objects.get(id = mid)
    context = {}
    if request.method == "POST":
        response = request.POST.get("response")
        email = request.POST.get("email")
        issue = FlaggedIssue(response=response,email=email, issued_object=material)
        issue.save()
        context["flag_id"] = issue.id
        messages.info(request, "Issue is reported successful.")
    return render(request, "app/flag_course.html", context)
    


def past_questions(request):
    courses = Course.objects.all().order_by("code")
    departments = Department.objects.all()
    sort = request.GET.get("sort")
    levels = [100, 200, 300, 400]
    
    context = {"departments":departments}
    context["levels"] = levels 
    context["courses"] = courses
    return render(request, 'app/pqs.html', context)
    
def download_material(request, material_id):
    try:
        # Fetch the material object by ID
        material = Material.objects.get(id=material_id)

        # Construct the file path using MEDIA_ROOT
        file_path = os.path.join(settings.MEDIA_ROOT, material.file.name)

        # Return the file as a response for download
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{os.path.basename(material.file.name)}"'
        material.increment_download_count()
        
        return response

    except Material.DoesNotExist:
        raise Http404("Material not found")
    except FileNotFoundError:
        raise Http404("File not found on the server")
    except Exception as e:
        raise Http404(f"Error processing the file: {e}")
        
        

def bulk_download_materials(request, id):
    # Get the course object or return 404 if not found
    course = get_object_or_404(Course, id=id)
    
    # Create a BytesIO buffer to store the ZIP file
    buffer = BytesIO()
    
    # Create a ZIP file in memory
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Loop through all materials related to the course
        for material in course.materials.all():
            # Get the file path and name
            file_path = material.file.path
            file_name = os.path.basename(file_path)
            
            # Add the file to the ZIP archive
            zip_file.write(file_path, file_name)
            material.increment_download_count()
    # Set the buffer's pointer to the beginning
    buffer.seek(0)
    
    # Create the HttpResponse object with the ZIP file
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{course.code.upper()}_materials.zip"'
    
    return response