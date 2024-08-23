from django.shortcuts import render, redirect
from .models import BlogPost, Rating
from .forms import BlogPostForm
from django.contrib import messages
# Create your views here.

def blogs(request):
  blogs = BlogPost.objects.all()
  return render(request, 'blog/index.html', {'blogs':blogs})
  
def read_blog(request, blog_id):
  blog = BlogPost.objects.get(id=blog_id)
  if request.method == 'POST':
    rating = request.POST.get('rating')
    comment = request.POST.get('feedback')
    blog.ratings.create(scale=int(float(rating)), comment=comment, user=request.user)
  user_id = request.user.id if request.user.is_authenticated else None
  user_rated = blog.user_rated(user_id)
  return render(request, 'blog/blog.html', {'blog':blog, 'user_rated':user_rated, 'rate': (1,2,3,4,5)})

def rate_blog(request, blog_id):
  if request.method != 'POST':
    return redirect('blog', blog_id)
  user = request.user if request.user.is_authenticated else None
  content = request.POST.get('content')
  rating = request.POST.get('rating')
  blog = BlogPost.objects.prefetch_related('ratings').get(id=blog_id)
  rating_obj = Rating.objects.create(user=user, content=content, rating=rating)
  blog.ratings.add(rating_obj)
  blog.save()
  return redirect('blog', blog_id)

def write_blog(request):
  form = BlogPostForm()
  if request.method == 'POST':
    content = request.POST.get('content')
    desc = request.POST.get('desc')
    title = request.POST.get('title')
    publish = request.POST.get('publish') == 'on'
    cover = request.FILES.get('cover')
    blog = BlogPost.objects.create(publish=publish, title=title, desc=desc, cover=cover, content=content, user=request.user)
    messages.success(request, 'Post saved.')
    return redirect('read_blog', blog.id)
  return render(request, 'blog/write.html', {'form':form})