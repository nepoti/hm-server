from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from re import match
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error
from response.templates import status_ok
from response.decorators import check_method
from response.decorators import check_method_auth


@csrf_exempt
@check_method('POST')
def register(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    if username is None or password is None or email is None:
        raise Http404
    if not match("^([a-zA-Z0-9_@\+\.\-]{1,30})$", username):
        return username_not_valid
    if User.objects.filter(username=username).exists():
        return username_already_exist
    if not match("^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$", email):
        return email_not_valid
    if User.objects.filter(email=email).exists():
        return email_already_exist
    user = User.objects.create_user(username, email, password)
    if user is None:
        return task_error
    return status_ok


@csrf_exempt
@check_method('POST')
def login(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            return status_ok
        return user_not_active
    elif request.POST.get('cookies', None) == 'true':
        return auth_error
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username is None or password is None:
        raise Http404
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return status_ok
        else:  # disabled
            return user_not_active
    else:  # login/password not valid
        return auth_error


@csrf_exempt
@check_method('POST')
def logout(request):
    auth_logout(request)
    return status_ok


@csrf_exempt
@check_method_auth('POST')
def email_change(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if password is None or email is None:
        raise Http404
    if not match("^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$", email):
        return email_not_valid
    if not request.user.check_password(password):
        return auth_error
    request.user.email = email
    request.user.save()
    return status_ok


@csrf_exempt
@check_method_auth('POST')
def pass_change(request):
    password = request.POST.get('password', None)
    new_password = request.POST.get('new_password', None)
    if password is None or new_password is None:
        raise Http404
    if not request.user.check_password(password):
        return auth_error
    request.user.set_password(new_password)
    request.user.save()
    user = authenticate(username=request.user.username, password=new_password)
    auth_login(request, user)
    return status_ok
