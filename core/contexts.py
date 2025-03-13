 
INFO = {
  "pr_long_name": "Abusite Hub",
  "pr_short_name": "Abusite Hub",
  "pr_small_logo": "imgs/logo.png" ,
  "pr_napss_logo": "imgs/tr_logo.png" ,
  "pr_big_logo": "",
  "pr_allowed_apps": ['admin', 'app', 'api', 'material', 'cbt'],
  "pr_allowed_views": ['wallet:generated_link'],
  "pr_app_maintenance": ['service', 'wallet',],
  "pr_view_maintenance": ['material:timetables'],
  "pr_only_staff_views": ['blog:write'],
}

def project_info(request):
  return INFO