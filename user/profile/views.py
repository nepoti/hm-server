from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from re import match
from response.templates import ok_response
from response.decorators import check_method_auth


@csrf_exempt
@check_method_auth('POST')
def read(request):
    return ok_response({"email": request.user.email})


@csrf_exempt
@check_method_auth('POST')
def update(request):
    raise Http404
