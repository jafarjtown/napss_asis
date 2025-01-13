# app/views.py
from django.shortcuts import render, redirect
from material.models import Material, Department , Course, PastQuestion, TimeTable
from blog.models import BlogPage, User
from .models import Newsletter, Partner
from django.contrib import messages
from .utils import search_in_model
def index(request):
  context = {}
  blogs = BlogPage.objects.all()
  context['blogs'] = blogs
  context['partners'] = Partner.objects.all()
  return render(request, 'app/index.html', context)

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')

def register_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, "This Email is already registered to our newsletter.")
            return redirect("/")
        n = Newsletter(email=email)
        n.save()
        
    return render(request, "app/email.html") 

def advance_search(request):
  if request.method != 'POST':
    return redirect('/')
  q = request.POST.get('q')
  pq = request.POST.get('pq', None)
  m = request.POST.get('m', None)
  c = request.POST.get('c', None)
  tb = request.POST.get('tb', None)
  bg = request.POST.get('bg', None)
  past_questions = search_in_model(PastQuestion, q) if pq else None
  materials = search_in_model(Material, q) if m else None
  courses = search_in_model(Course, q) if c else None
  time_tables = search_in_model(TimeTable, q) if tb else None
  blogs = search_in_model(BlogPage, q) if bg else None
  models = (past_questions, materials, courses, time_tables)
  context = {'models_name': [], 'empty_models': [], 'models': [], 'q': q, 'number_of_results': 0}
  
  for model in models:
    if model != None:
      context['models_name'] += [model.model._meta.object_name]
      if not model:
        context['empty_models'] += [model.model._meta.object_name]
      else:
        context['models'] += [{'object_name':model.model._meta.object_name, 'objects': model}]
        context['number_of_results'] += model.count()
  return render(request, 'advance_search.html', context)