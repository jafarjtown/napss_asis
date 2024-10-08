# app/views.py
from django.shortcuts import render, redirect
from material.models import Material, Department , Course
from blog.models import BlogPost, User
from .models import Newsletter, Partner
from django.contrib import messages

def index(request):
  context = {}
  blogs = BlogPost.objects.all()
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
