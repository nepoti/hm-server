from django.http import Http404
from templates import auth_error
from templates import user_not_active

def check_method(method):
    def my_decorator(function):
        def wrapper(request):
            if request.method != method:
                raise Http404
            return function(request)
        return wrapper
    return my_decorator

def check_method_auth(method):
    def my_decorator(function):
        def wrapper(request):
            if request.method != method:
                raise Http404
            if not request.user.is_authenticated():
                return auth_error
            elif not request.user.is_active:
                return user_not_active
            return function(request)
        return wrapper
    return my_decorator
