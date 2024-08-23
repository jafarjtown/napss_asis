from django.forms import ModelForm
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from .models import BlogPost
class BlogPostForm(ModelForm):
  content = SummernoteTextField()
  class Meta:
    model = BlogPost
    fields = ['content']