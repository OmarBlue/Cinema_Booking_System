from django.shortcuts import redirect,resolve_url
from django.contrib import messages
from functools import wraps

def is_superuser(user):
    if user.is_authenticated and user.user_type == 0:
        return True
    return False

def is_cinema_manager(user):
    if (user.is_authenticated and user.user_type == 1) or  (user.is_authenticated and user.user_type == 0):
        return True
    return False

def is_account_manager(user):
    if (user.is_authenticated and user.user_type == 2) or (user.is_authenticated and user.user_type == 0):
        return True
    return False

def is_student(user):
    if user.is_authenticated and user.user_type == 3:
        return True
    return False

def is_club_rep(user):
    if user.is_authenticated and user.user_type == 4:
        return True
    return False

def is_club_rep_or_student(user):
    if (user.is_authenticated and user.user_type == 3) or (user.is_authenticated and user.user_type == 4):
        return True
    return False

def user_passes_test_custom(test_func, login_url=None, message=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            if message:
                request.session['permission_denied_message'] = message
            return redirect(login_url)
        return _wrapped_view
    return decorator

