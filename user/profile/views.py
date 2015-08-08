from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from response.templates import ok_response, invalid_data
from response.decorators import check_method_auth, check_headers_version
from user.models import UserProfile
from json import loads


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
def read(request):
    user_id = request.POST.get('id', None)
    try:
        if user_id:
            user_id = int(user_id)
            return ok_response(UserProfile.objects.filter(id=user_id)[0].get_info())
        else:
            user_id = request.user.id
            return ok_response(UserProfile.objects.filter(user_id=user_id)[0].get_info())
    except:
        return invalid_data


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
def update(request):
    data = request.POST.get('data', None)
    if data is None:
        raise Http404
    try:
        data = loads(data)
    except:
        return invalid_data
    return UserProfile.objects.filter(user_id=request.user.id)[0].set_info(data)
