from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages 
from .contexts import INFO

class OnlyStaffViewMiddleware(MiddlewareMixin):
  def process_view(self, request, view_func, view_args, view_kwargs):
    view_name = request.resolver_match.view_name
    if view_name in INFO.get('pr_only_staff_views', []) and request.user.is_staff == False:
      messages.error(request, f'Please Sign Up to Staff Account')
      return redirect(reverse('auth:user_login')+f"?next={request.path}")
    return None
    
class LoginRequiredOrNotMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = request.resolver_match.view_name
        app_name = request.resolver_match.app_names[0] if request.resolver_match.app_names else None
        if app_name == None:
          return None
        user = request.user
        if app_name == 'auth' or INFO.get('pr_allowed_apps', 'all') == 'all':
          return None
        if app_name in INFO.get('pr_app_maintenance'):
          messages.info(request, f'The page is under maintenance, try again later.\nThanks')
          return redirect('app:index')
        if view_name in INFO.get('pr_allowed_views'):
          return None
        if not user.is_authenticated and not app_name in INFO.get('pr_allowed_apps'):
          messages.error(request, f'Please Sign Up to have access to the page.')
          return redirect(reverse('auth:user_login')+f"?next={request.path}")
        return None