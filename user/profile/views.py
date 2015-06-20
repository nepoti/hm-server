from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from re import match


@csrf_exempt
def read(request):
    if request.method != 'POST':
        raise Http404
    if request.user.is_authenticated():
        if request.user.is_active:
            return JsonResponse({"status": 1, "result": {"email": request.user.email}, "error": 0})
        return HttpResponse('{"status": 0, "error": 42}')
    return HttpResponse('{"status": 0, "error": 41}')


def update(request):
    raise Http404
