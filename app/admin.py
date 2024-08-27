from django.contrib import admin
from core.contexts import INFO

admin.site.site_header = INFO.get('pr_short_name')
admin.site.site_title = f"{INFO.get('pr_short_name')} Administrator"
admin.site.index_title = f"Welcome to {INFO.get('pr_long_name')}, ABU Administrator Panel"

