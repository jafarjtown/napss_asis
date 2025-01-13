from django.contrib import admin
from .models import BlogPage, Document, Tag
# Register your models here.

admin.site.register(BlogPage)
admin.site.register(Document)
admin.site.register(Tag)

