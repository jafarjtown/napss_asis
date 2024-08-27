 
INFO = {
  "pr_long_name": "National Association of Political Science Student & Association of Student in International Studies",
  "pr_short_name": "NAPSS & ASIS",
  "pr_small_logo": "imgs/small_logo.jpg" ,
  "pr_big_logo": "",
  "pr_allowed_apps": ['admin', 'app', 'api', 'material'],
  "pr_app_maintenance": [],
  "pr_only_staff_views": ['blog:write'],
}

def project_info(request):
  return INFO