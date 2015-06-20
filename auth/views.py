from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from re import match


def index(request):
    #from django.core.servers.basehttp import FileWrapper
    #response = HttpResponse(FileWrapper(open('/home/hm/auth/test.tar.gz')), content_type='application/x-tar')
    #response['Content-Disposition'] = 'attachment; filename=test.tar.gz'
    #return response
    raise Http404


@csrf_exempt
def register(request):
    if request.method!='POST':
        raise Http404
    userName=request.POST.get('username',None)
    userPass=request.POST.get('password',None)
    userMail=request.POST.get('email',None)
    if userName is None or userPass is None or userMail is None:
        raise Http404
    if not match("^([a-zA-Z0-9_@\+\.\-]{1,30})$",userName):
        return HttpResponse('{"status": 0, "error": 11}')
    if User.objects.filter(username=userName).exists():
        return HttpResponse('{"status": 0, "error": 12}')
    if not match("^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$",userMail):
        return HttpResponse('{"status": 0, "error": 31}')
    if User.objects.filter(email=userMail).exists():
        return HttpResponse('{"status": 0, "error": 32}')
    user=User.objects.create_user(userName,userMail,userPass)
    if user is None:
        return HttpResponse('{"status": 0, "error": 41}')
    return HttpResponse('{"status": 1, "error": 0}')


@csrf_exempt
def login(request):
    if request.method!='POST':
        raise Http404
    if request.user.is_authenticated():
     if request.user.is_active:
      return JsonResponse({"status": 1, "result": {"email": request.user.email}, "error": 0})
     return HttpResponse('{"status": 0, "error": 42}')
    elif request.POST.get('cookies',None)=='true':
     return HttpResponse('{"status": 0, "error": 41}')
    userName=request.POST.get('username',None)
    userPass=request.POST.get('password',None)
    if userName is None or userPass is None:
        raise Http404
    user = authenticate(username=userName, password=userPass)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
	    return JsonResponse({"status": 1, "result": {"email": user.email}, "error": 0})
        else:#disabled
            return HttpResponse('{"status":0, "error":42}')
    else:#login/password not valid
        return HttpResponse('{"status":0, "error":41}')


def logout(request):
    auth_logout(request)
    return HttpResponse('')


def is_logged_in(request):
    if request.user.is_authenticated():
    	return HttpResponse('yes')
    return HttpResponse('no')


def temp(request):
    from django.core.mail import send_mail
    send_mail('Subject here', 'Here is the message.', 'devtest1997@yandex.ru',
        ['oagromyak@gmail.com'], fail_silently=False)
    return HttpResponse('no')

@csrf_exempt
def email_change(request):
    if request.method!='POST':
     raise Http404
    userMail=request.POST.get('email',None)
    if userMail is None:
     raise Http404
    if request.user.is_authenticated():
     if request.user.is_active:
      if not match("^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$",userMail):
       return HttpResponse('{"status": 0, "error": 31}')
      request.user.email=userMail
      request.user.save()
      return HttpResponse('{"status": 1, "error": 0}')
     return HttpResponse('{"status": 0, "error": 42}')
    return HttpResponse('{"status": 0, "error": 41}')


@csrf_exempt
def get_email(request):
    if request.method!='GET':
     raise Http404
    if request.user.is_authenticated():
     return HttpResponse('{"status": 1, "result": '+request.user.email+', "error": 0}')
    return HttpResponse('{"status": 0, "result": "", "error": 41}')


@csrf_exempt
def pass_change(request):
 if request.method!='POST':
  raise Http404
 userPass=request.POST.get('password',None)
 if userPass is None:
  raise Http404
 if request.user.is_authenticated():
  if request.user.is_active:
   request.user.set_password(userPass)
   request.user.save()
   user=authenticate(username=request.user.username,password=userPass)
   auth_login(request,user)
   return HttpResponse('{"status": 1, "error": 0}')
  return HttpResponse('{"status": 0, "error": 42}')
 return HttpResponse('{"status": 0, "error": 41}')
