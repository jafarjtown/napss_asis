from django.shortcuts import render, redirect
from django.db.models import Q
from .models import BlogPage, BloggerSite, Document, Tag, BlogComment
# Create your views here.
def index(request):
  q = request.GET.get('q', '')
  blogs = BlogPage.objects.filter(Q(title__icontains=q)|Q(content__icontains=q),is_publish=True)
  
  return render(request, 'blog/blog_index_page.html', {'blogs': blogs, 'q': q})
def blog_list(request):
  blogs = BlogPage.objects.all()
  return render(request, 'blog/post-list.html', {'blogs': blogs})

def view_blog(request, slug):
  context = {}
  page = BlogPage.objects.get(slug=slug)
  context['page'] = page
  return render(request, 'blog/blog.html', context)


def edit_blog(request, slug):
  context = {}
  blog_site, _ = BloggerSite.objects.get_or_create(owner=request.user)
  tags = Tag.objects.all()
  blog = BlogPage.objects.get(slug=slug)
  pages = BlogPage.objects.all()
  context['documents'] = blog_site.documents
  context['blog'] = blog
  context['tags'] = tags
  context['pages'] = pages
  if request.method == "POST":
    data = request.POST
    title = data.get('title')
    content = data.get('content')
    cover = data.get('cover_image')
    
    allow_comment = data.get('allow_comment', False)
    save_as_draft = data.get('draft', False)
    
    galleries = data.getlist('galleries')
    tag_ids = data.getlist('tags')
    
    _tags = tags.filter(id__in=tag_ids)
    documents = blog_site.documents.filter(id__in=galleries)
    cover_image = blog_site.documents.get(id=cover)
    blog.cover_image = cover_image
    blog.title = title
    blog.content = content
    blog.allow_comment = True if allow_comment else False
    blog.is_publish = False if save_as_draft else True
    blog.gallery_images.clear()
    for doc in documents:
      blog.gallery_images.add(doc)
    blog.tags.clear()
    for tag in _tags:
      blog.tags.add(tag)
    
    blog.save()
  return render(request, 'blog/edit-blog.html', context)

def add_blog(request):
  context = {}
  blog_site, _ = BloggerSite.objects.get_or_create(owner=request.user)
  tags = Tag.objects.all()
  pages = BlogPage.objects.all()
  context['documents'] = blog_site.documents
  context['tags'] = tags
  context['pages'] = pages
  if request.method == "POST":
    data = request.POST
    title = data.get('title')
    content = data.get('content')
    cover = data.get('cover_image')
    
    allow_comment = data.get('allow_comment')
    save_as_draft = data.get('draft')
    
    galleries = data.getlist('galleries')
    tag_ids = data.getlist('tags')
    
    _tags = tags.filter(id__in=tag_ids)
    documents = blog_site.documents.filter(id__in=galleries)
    cover_image = blog_site.documents.get(id=cover)
    blog = BlogPage.objects.create(title=title, content=content, author=request.user, cover_image=cover_image)
    
    if allow_comment:
      blog.allow_comment = True
    if save_as_draft:
      blog.is_publish = False
    
    for doc in documents:
      blog.gallery_images.add(doc)
    for tag in _tags:
      blog.tags.add(tag)
    
    blog.save()
  return render(request, 'blog/page-add.html', context)

def comment_blog(request, page_id):
  page = BlogPage.objects.get(id=page_id)
  if request.method == 'POST':
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    content = request.POST.get('content', '')
    BlogComment.objects.create(blog=page, name=name, email=email, content=content)
  return redirect('blog:read_blog', page.slug)

def media_gallery(request):
  context = {}
  blog_site, _ = BloggerSite.objects.get_or_create(owner=request.user)
  context['documents'] = blog_site.documents
  return render(request, 'blog/media.html', context)

def add_media_gallery(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    alt_text = request.POST.get('alt_text')
    document = request.FILES.get('document')
    blog_site, _ = BloggerSite.objects.get_or_create(owner=request.user)
    doc = Document.objects.create(name=name, alt_text=alt_text, file=document)
    blog_site.documents.add(doc)
    blog_site.save()
  return redirect('blog:media')

def update_media_gallery(request, doc_id):
  if request.method == 'POST':
    name = request.POST.get('name')
    alt_text = request.POST.get('alt_text')
    document = request.FILES.get('document')
    blog_site, _ = BloggerSite.objects.get_or_create(owner=request.user)
    if blog_site.documents.filter(id=doc_id).exists():
      doc = blog_site.documents.get(id=doc_id)
      doc.name=name
      doc.alt_text=alt_text
      if document:
        doc.file = document
      doc.save()
  return redirect('blog:media')