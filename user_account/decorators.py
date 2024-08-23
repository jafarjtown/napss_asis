from functools import wraps
from django.http import JsonResponse

def has_enough_coins(minimum_coins):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.account.coins >= minimum_coins:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'error': 'Not enough coins'}, status=403)
        return _wrapped_view
    return decorator
    
def subtract_coins(amount):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.account.coins >= amount:
                try:
                    user.account.coins -= amount
                    user.account.save()
                    return view_func(request, *args, **kwargs)
                except Exception as e:
                    user.account.coins += amount
                    user.account.save()
                    return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
            else:
                return JsonResponse({'error': 'Not enough coins'}, status=403)
        return _wrapped_view
    return decorator