from django.shortcuts import render, redirect 
from django.http import JsonResponse 
from .models import CourseCBT, Question, Option, EssayQuestion,TrueFalseQuestion
from .forms import QuestionForm, OptionForm, TrueFalseQuestionForm
from material.models import Department , Course

from user_account.decorators import has_enough_coins, subtract_coins
import random as r
import json
# Create your views here.

def index(request):
    return render(request, "cbt/index.html")

def tests(request):
    context = {}
    departments = Department.objects.all()
    course = request.GET.get("course", None)
    department = request.GET.get("department", 0)
    level = request.GET.get("level", 0)
    levels = [100, 200, 300, 400]
    context["level"] = int(level)
    context["department"] = int(department)
    context["departments"] = departments
    context["levels"] = levels
    if course:
      context['course'] = Course.objects.prefetch_related('objectives').get(code=course)
    return render(request, "cbt/cbt_tests.html", context)

#@has_enough_coins(100)
#@subtract_coins(100)
def cbt_test(request, id=None):
    t = int(request.GET.get("t", 15))
    course = Course.objects.get(id=id)
    questions= course.objectives.order_by("?").all()
    return render(request, "cbt/cbt_test.html", {"course": course, "qs": questions[:t]})
    
def cbt_time_base(request, id=None):
    time = int(request.GET.get("t", 15))
    if time == 15 or time < 20:
        t = 30
    elif time == 20 or time < 35:
        t = 40
    else:
        t = 60
    course = Course.objects.get(id=id)
    questions= course.objectives.order_by("?").all()
    return render(request, "cbt/cbt_time_base.html", {"course": course, "qs": questions[:t], "time":time})
    
    
def cbt_test_result(request, id):
    result = {"score":0, "qss":{}}
    course = Course.objects.get(id=id)
    qs = []
    if request.method == "POST":  
        attempts = dict(request.POST)
        del attempts["csrfmiddlewaretoken"]
        for q, a in attempts.items():
            a = int(a[0])
            qq = course.objectives.get(id = q)
            op = qq.options.get(id=a)
            qs.append({"q":qq, "select": a})
            if op.is_correct:
                result["score"] += 1
    return render(request, "cbt/cbt_time_base_result.html", {"course": course, "qs": qs, "result": result})


def cbt_create_course(request):
    courses = CourseCBT.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        course,_ = cbt.objects.get_or_create(name=name)
        return redirect("cbt:cbt_add_qs", course=course.id)
    return render(request, 'cbt/add_course.html', {"courses":courses})
    
def cbt_add_qs(request, course):
    course = CourseCBT.objects.get(id=course)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_forms = []
        for key, value in request.POST.items():
        
            if key.startswith('option_') and key.endswith("value"):
                option_number = key.split("_")[1].split("-")[0]
                option_form = OptionForm(request.POST, prefix=f"option_{option_number}")
                option_forms.append(option_form)            
        option_forms = [OptionForm(request.POST, prefix=f'option_{i}') for i in range(4)]
        if question_form.is_valid() and len(option_forms) > 0:
            question = question_form.save()
            course.questions.add(question)
            course.save()
            option_forms = [option_form for option_form in option_forms if option_form.is_valid()]
            for option_form in option_forms:
                option = option_form.save()
                question.options.add(option)
                question.save()
            return redirect("cbt:cbt_add_qs", course=course.id)
    else:
        question_form = QuestionForm()
        option_forms = [OptionForm(prefix=f'option_{i}') for i in range(4)]
    return render(request, "cbt/add_qs.html", {"course":course, 'question_form': question_form, 'option_forms': option_forms})


def add_by_upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if uploaded_file:
                js = json.load(uploaded_file)
                course = Course.objects.get(code=js.get('course'))
                #  co = CourseCBT.objects.get(course__code=js.get("course"))
                for q in js.get("questions"):
                    if course.objectives.filter(question=q["question"]).exists():
                        continue 
                    qu = Question.objects.create(question=q["question"])
                    for op in q.get("options"):
                        is_correct = False
                        if q["answer"] == op:
                            is_correct = True
                        o = Option.objects.create(value=op, is_correct=is_correct)
                        qu.options.add(o)
                        qu.save()
                    course.objectives.add(qu)
                    course.save()
        else:
            return JsonResponse({"error": "No file uploaded"}, status=400)
    return redirect("cbt:cbt")


def essay_cbt(request):
    courses = EssayTest.objects.all()
    return render(request, "cbt/essay_cbt.html", {"courses":courses})
    
def add_by_upload_essay(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if uploaded_file:
              js = json.load(uploaded_file)
              for topic in js:
                  co, cr = EssayTest.objects.get_or_create(topic=topic.get("Topic"))
                  if cr:
                      co.note = topic.get("Essay")
                  for q in topic.get("Questions"):
                      if co.questions.filter(question=q).exists():
                            continue 
                      qu = EssayQuestion.objects.create(question=q)
                      co.questions.add(qu)
                      co.save()
        else:
            return JsonResponse({"error": "No file uploaded"}, status=400)
    return redirect("essay_cbt")

def cbt_create_course_essay(request):
    if request.method == "POST":
        name = request.POST.get("name")
        course = EssayTest.objects.get_or_create(name=name)
        return redirect("cbt_add_qs", course=course.id)
    return render(request, 'cbt/upload_essay_qs.html')
    
#@has_enough_coins(50)
#@subtract_coins(50)    
def cbt_test_essay(request, id=None):
    course = CourseCBT.objects.get(id=id)
    questions= course.essays.order_by("?").all()
    return render(request, "cbt/cbt_test_essay.html", {"course": course, "qs": questions[:6]})
    

def true_false_test(request):
    course = CourseCBT.objects.get(id=id)
    questions= course.true_false.order_by("?").all()
    return render(request, "cbt/tf.html", {"questions":questions, 'course':course})
    
def true_false_result(request, tid):
    course = CourseCBT.objects.get(id=tid)
    questions= course.true_false.order_by("?").all()
    return render(request, 'cbt/tfr.html', {"questions": questions, "course":course})

def create_true_false_question(request, course):
    if request.method == 'POST':
        course = TrueFalseCourse.objects.get(id=course)
        form = TrueFalseQuestionForm(request.POST)
        if form.is_valid():
            trf = form.save(commit=False)
            trf.course = course
            trf.save()
            return redirect('cbt_add_tr_qs', course=course.id)
    else:
        form = TrueFalseQuestionForm()

    return render(request, 'cbt/true_question_form.html', {'form': form})
    
def fill_in_blank(request, id):
    course = CourseCBT.objects.get(id=id)
    questions= course.fill_the_blank.order_by("?").all()
    return render(request, 'cbt/fill-in-blank.html', {"questions":questions, 'course':course})
