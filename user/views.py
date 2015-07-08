from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from response.templates import auth_error
from response.templates import status_ok
from response.decorators import check_method_auth


@csrf_exempt
@check_method_auth('POST')
def remove(request):
    password = request.POST.get('password', None)
    if password is None:
        raise Http404
    if not request.user.check_password(password):
        return auth_error
    request.user.is_active = False
    request.user.save()
    auth_logout(request)
    return status_ok
