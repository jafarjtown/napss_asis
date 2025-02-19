from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Base model for content types
class Content(models.Model):
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  
  @property
  def edit_template(self):
    return self.content_object.edit_template()

class BaseContent(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        raise NotImplementedError("Subclasses must implement this method.")


# Define models for different types of content
class TextContent(BaseContent):
    text = models.TextField()

    def get_display_name(self):
        return self.text[:50]  # Return first 50 characters of the text
    
    def get_content(self):
      return self.text
      
    def edit_template(self):
      return 'text_edit.html'

class ImageContent(BaseContent):
    image = models.FileField(upload_to='images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    width = models.IntegerField(default=200)
    height = models.IntegerField(default=200)
    gravity = models.CharField(max_length=20, default='start')
    def get_display_name(self):
        return self.caption or "Image"
        
    def get_content(self):
      return f'''<div class='d-flex flex-column justify-content-{self.gravity}'>
            <img width='{self.width}' height='{self.height}' style='object-fit:contain' src="{self.image.url}">
            <p>{self.caption}</p>
          </div>'''


class VideoContent(BaseContent):
    video_url = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def get_content(self):
      return f'<div><video style="width:100%" src="{self.video_url}" controls /><p>{self.description}</p></div>'

    
    
    def get_display_name(self):
        return self.description or "Video"


class ListContent(BaseContent):
    items = models.TextField(help_text="Enter items as a comma-separated list")

    def get_display_name(self):
        return self.items[:50]  # Return first 50 characters of the list


class LinkContent(BaseContent):
    url = models.URLField()
    title = models.CharField(max_length=255)

    def get_display_name(self):
        return self.title
    def get_content(self):
      return f'<a href="{self.url}">{self.title}</a>'


class BookSubSection(models.Model):
    title = models.CharField(max_length=255)
    contents = models.ManyToManyField(Content)


    
    def __str__(self):
        return self.title


class BookSection(models.Model):
    title = models.CharField(max_length=255)
    subsections = models.ManyToManyField(BookSubSection, related_name='sections')
    contents = models.ManyToManyField(Content)

    def __str__(self):
        return self.title
        
      
class Book(models.Model):
    title = models.CharField(max_length=255)
    sections = models.ManyToManyField(BookSection, related_name='books', blank=True)

    def headers(self):
        """Return a list of all section and subsection titles in the book."""
        headers = []
        for section in self.sections.all():
            headers.append(section.title)
            for subsection in section.subsections.all():
                headers.append(subsection.title)
        return headers

    def __str__(self):
        return self.title