# This file is modified from https://stackoverflow.com/a/6777372.
# Created by LvanderRee (https://stackoverflow.com/users/853750/lvanderree)
# and Aleksei Khatkevich (https://stackoverflow.com/users/11251373/aleksei-khatkevich).
# Licensed under Creative Commons BY-SA 4.0. https://creativecommons.org/licenses/by-sa/4.0/

from functools import wraps
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
import django.contrib.auth.decorators as django_decorators
from django.core.exceptions import PermissionDenied

default_message = "You are not authorised to view this page."
default_message_login_required = "Please login to access this page."

def user_passes_test_set_message(test_func, message=default_message):
    """
    Decorator for views that checks that the user passes the given test,
    setting a message in case of no success. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, message)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, message=default_message):
    decorator1 = user_passes_test_set_message(test_func, message)
    decorator2 = django_decorators.user_passes_test(test_func, login_url, redirect_field_name)
    return lambda view_func: decorator1(decorator2(view_func))

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None, message=default_message_login_required):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url, redirect_field_name, message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def api_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view