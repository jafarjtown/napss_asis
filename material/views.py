from django.shortcuts import render,redirect
from django.http import JsonResponse 
from django.http import FileResponse, Http404
import os
from .models import Material, Department , Course, TimeTable, CourseComment ,PastQuestion, Day, Time
from user_account.models import FlaggedIssue
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import FileComparator
from blog.models import BlogPage, User
# Create your views here.

    
def upload(request):
    context = {
            "departments": Department.objects.all()
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
            except Exception as e:
                print(e)
            messages.success(request, "Material added successful")


    return render(request, 'app/upload.html', context)


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

        # Get the file path
        file_path = material.file.path

        # Return the file as a response for download
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{material.file.name}"'
        user_wallet = request.user.wallet 
        user_wallet.amount -= 50
        user_wallet.save()
        print(user_wallet)
        return response

    except Material.DoesNotExist:
        raise Http404("Material not found")
    except Exception as e:
        raise Http404("Error processing the file")