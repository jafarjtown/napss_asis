# core/templatetags/breadcrumbs.py

from django import template
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    request = context['request']
    view_name = resolve(request.path).view_name
    breadcrumbs = [{'name': 'Home', 'url': reverse('index')}]

    if view_name == 'home':
        return mark_safe('<li class="breadcrumb-item active">Home</li>')
    
    if view_name:
        for part in request.path.strip('/').split('/'):
            url = reverse(part) if part else '/'
            breadcrumbs.append({'name': part.capitalize(), 'url': url})

    return mark_safe(''.join([
        f'<li class="breadcrumb-item"><a href="{crumb["url"]}">{crumb["name"]}</a></li>' 
        if i < len(breadcrumbs) - 1 else 
        f'<li class="breadcrumb-item active">{crumb["name"]}</li>'
        for i, crumb in enumerate(breadcrumbs)
    ]))