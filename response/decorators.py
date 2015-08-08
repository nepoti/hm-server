from django.http import Http404
from templates import auth_error
from templates import user_not_active
from templates import old_client_error
import constants as c


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


def check_methods_auth(methods):
    def my_decorator(function):
        def wrapper(request):
            if request.method not in methods:
                raise Http404
            if not request.user.is_authenticated():
                return auth_error
            elif not request.user.is_active:
                return user_not_active
            return function(request)
        return wrapper
    return my_decorator


def check_headers_version(function):
    def my_decorator(request):
            platform = request.META.get('HTTP_X_PLATFORM', None)
            platform_version = request.META.get('HTTP_X_PLATFORM_VERSION', None)
            client_version = request.META.get('HTTP_X_CLIENT_VERSION', None)
            if platform is None or platform_version is None or client_version is None:
                raise Http404
            if platform not in c.CLIENT_PLATFORMS:
                raise Http404
            if client_version < c.CLIENT_MIN_VERSION[platform]:
                return old_client_error
            return function(request)
    return my_decorator
