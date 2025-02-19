from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, TextContent, Content, BookSubSection, BookSection, ImageContent, LinkContent, VideoContent
# Create your views here.

def index(request):
  return render(request, 'reader/index.html')

def new(request):
  book = Book.objects.first()
  last_section = book.sections.last()
  
  
  return render(request, 'reader/reader.html', {'book': book})

def edit(request, content_id):
  content = Content.objects.get(id=content_id)
  
  if request.method == 'POST':
    text = request.POST.get('text')
    if len(text) > 0:
      content.content_object.text = text
      content.content_object.save()
      return render(request, f'reader/reader.html#text-content', {'content': content})
    else:
      content.content_object.delete()
      content.delete()
      return HttpResponse('Deleted')
  
  return render(request, f'reader/edit/{content.edit_template}', {'content': content})

def edit_title(request, id):
  context = {}
  subsection = request.GET.get('subsection', None)
  if subsection:
    content = BookSubSection.objects.get(id=id)
    context['sub'] = True
  else:
    content = BookSection.objects.get(id=id)
  context['content'] = content
  if request.method == 'POST':
    text = request.POST.get('title')
    if len(text) > 0:
      c = {}
      content.title = text
      content.save()
      if subsection:
        c['subsection'] = content
        v = 'sub-topic'
      else:
        c['section'] = content
        v = 'topic'
      return render(request, f'reader/reader.html#{v}', c)
    else:
      content.delete()
      return HttpResponse(status=204)
  
  return render(request, f'reader/edit/edit_title.html', context)

def update_book(request, section_id, block):
  book = Book.objects.first()
  title = None
  stitle = None
  
  if block == 'section':
    section = book.sections.get(id=int(section_id))
    stitle = request.POST.get('stitle', None)
    title = request.POST.get('title', None)
    pass
  else:
    section = BookSubSection.objects.get(id=int(section_id))
  if request.method == 'POST':
    text = request.POST.get('text', None)
    image = request.FILES.get('image', None)
    link = request.POST.get('link', None)
    video = request.POST.get('video', None)
    
    if title:
      book.sections.create(title=title)
      return HttpResponse(f'<h2>{title}<h2/>')

    if stitle:
      # book.sections.create(title=title)
      
      section.subsections.create(title=stitle)
      
    if text:
      
      text_content = TextContent.objects.create(text=text)
      content = Content.objects.create(content_object=text_content)
      
      section.contents.add(content)
    
    if image:
      caption = request.POST.get('caption', '')
      width = request.POST.get('width', 200)
      height = request.POST.get('height', 200)
      gravity = request.POST.get('gravity', 'center')
      image_content = ImageContent.objects.create(image=image, caption=caption, gravity=gravity, width=width, height=height)
      content = Content.objects.create(content_object=image_content)
      section.contents.add(content)
    if link:
      name = request.POST.get('name')
      link_content = LinkContent.objects.create(url=link, title=name)
      content = Content.objects.create(content_object=link_content)
      section.contents.add(content)
    if video:
      description = request.POST.get('description')
      video_content = VideoContent.objects.create(video_url=video, description=description)
      content = Content.objects.create(content_object=video_content)
      section.contents.add(content)
  if block == 'section':
    return render(request, 'reader/reader.html#section', {'section': section})
  else:
    return render(request, 'reader/reader.html#subsection', {'subsection': section})

def snippet(request):
  type = request.GET.get('type', None)
  block = request.GET.get('block', None)
  id = request.GET.get('id', None)
  context = {'block': block, 'id': id}
  
  return render(request, f'reader/snippet/{type}.html', context)