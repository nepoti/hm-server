from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from re import match
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, status_ok
from response.decorators import check_method, check_method_auth, check_headers_version
import constants as c
from django.views.decorators.gzip import gzip_page


@csrf_exempt
@check_method('POST')
@check_headers_version
def register(request):
    phone = request.POST.get('phone', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    if phone is None or password is None or email is None:
        raise Http404
    if not c.is_valid_phone(phone):
        return username_not_valid
    if User.objects.filter(username=phone).exists():
        return username_already_exist
    if not match(c.REGEX_EMAIL, email):
        return email_not_valid
    if User.objects.filter(email=email).exists():
        return email_already_exist
    user = User.objects.create_user(phone, email, password)
    if user is None:
        return task_error
    return status_ok


def login_user(username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


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
    user = login_user(username=username, password=password)
    if user is not None:
        if user.is_active:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            return status_ok
        else:  # disabled
            return user_not_active
    else:  # login/password not valid
        return auth_error


@check_method('POST')
@check_headers_version
def logout(request):
    auth_logout(request)
    return status_ok


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


from django.contrib.auth.views import password_reset_confirm
from django.core.urlresolvers import reverse
from django.shortcuts import render
from tasks.tasks import send_reset_mail


@csrf_exempt
@check_method('POST')
@check_headers_version
def restore(request):
    email = request.POST.get('email', None)
    if email is None:
        raise Http404
    if not match(c.REGEX_EMAIL, email):
        return email_not_valid
    send_reset_mail.delay(email)
    return status_ok


@gzip_page
def restore_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='reset_confirm.html',
                                  uidb64=uidb64, token=token, post_reset_redirect=reverse('success2'))

@gzip_page
def success2(request):
    return render(request, "success2.html")


