from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from re import match
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from response.decorators import check_method, check_method_auth, check_headers_version
from user.models import UserProfile
from json import loads
import constants as c


@csrf_exempt
@check_method('POST')
@check_headers_version
def register(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    if username is None or password is None or email is None:
        raise Http404
    if not match(c.REGEX_USERNAME, username):
        return username_not_valid
    if User.objects.filter(username=username).exists():
        return username_already_exist
    if not match(c.REGEX_EMAIL, email):
        return email_not_valid
    if User.objects.filter(email=email).exists():
        return email_already_exist
    user = User.objects.create_user(username, email, password)
    user_profile = UserProfile.objects.create(user=user, name=user.username)
    if user is None or user_profile is None:
        return task_error
    return status_ok


@csrf_exempt
@check_method('POST')
@check_headers_version
def login(request):
    if request.POST.get('cookies', None) == 'true':
        if request.user.is_authenticated():
            if request.user.is_active:
                return status_ok
            return user_not_active
        else:
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
@check_headers_version
def logout(request):
    auth_logout(request)
    return status_ok


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
def edit(request):
    password = request.POST.get('password', None)
    username = request.POST.get('username', None)
    new_password = request.POST.get('new_password', None)
    email = request.POST.get('email', None)
    if password is None or (username is None and new_password is None and email is None):
        raise Http404
    if username:
        if not match(c.REGEX_USERNAME, username):
            return username_not_valid
        if User.objects.filter(username=username).exists():
            return username_already_exist
    if email:
        if not match(c.REGEX_EMAIL, email):
            return email_not_valid
        if User.objects.filter(email=email).exists():
            return email_already_exist
    if not request.user.check_password(password):
        return auth_error
    if username:
        request.user.username = username
    if email:
        request.user.email = email
    if new_password:
        request.user.set_password(new_password)
    request.user.save()
    if new_password:
        user = authenticate(username=request.user.username, password=new_password)
        auth_login(request, user)
    return status_ok
