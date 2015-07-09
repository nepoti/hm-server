from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from response.templates import ok_response
from response.decorators import check_method_auth
from user.models import UserProfile
from json import loads


@csrf_exempt
@check_method_auth('POST')
def read(request):
    return ok_response(UserProfile.objects.filter(user_id=request.user.id)[0].get_info())


@csrf_exempt
@check_method_auth('POST')
def update(request):
    data = request.POST.get('data', None)
    if data is None:
        raise Http404
    try:
        data = loads(data)
    except:
        raise Http404
    return UserProfile.objects.filter(user_id=request.user.id)[0].set_info(data)
