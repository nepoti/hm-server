from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def remove(request):
    if request.method!='POST':
        raise Http404
    userPass=request.POST.get('password',None)
    if userPass is None:
        raise Http404
    if request.user.is_authenticated():
        if request.user.is_active:
            if not request.user.check_password(userPass):
                return HttpResponse('{"status": 0, "error": 41}')
            request.user.is_active=False
            request.user.save()
            logout(request)
            return HttpResponse('{"status": 1, "error": 0}')
        return HttpResponse('{"status": 0, "error": 42}')
    return HttpResponse('{"status": 0, "error": 41}')
