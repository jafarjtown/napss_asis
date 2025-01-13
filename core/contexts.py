 
INFO = {
  "pr_long_name": "National Association of Political Science Student & African Society of International Studies E-Library",
  "pr_short_name": "NAPSS & ASIS E-Library",
  "pr_small_logo": "imgs/small_logo.jpg" ,
  "pr_napss_logo": "imgs/napss.jpg" ,
  "pr_big_logo": "",
  "pr_allowed_apps": ['admin', 'app', 'api', 'material'],
  "pr_app_maintenance": [],
  "pr_view_maintenance": ['material:timetables'],
  "pr_only_staff_views": ['blog:write'],
}

def project_info(request):
  return INFO