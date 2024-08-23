from django.contrib import admin
from .models import BlogPost, Rating
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(BlogPost, PostAdmin)
# admin.site.register(BlogPost)
admin.site.register(Rating)