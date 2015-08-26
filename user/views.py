from django.http import Http404
from django.contrib.auth import logout as auth_logout
from response.templates import auth_error, status_ok
from response.decorators import check_method_auth, check_headers_version


@check_method_auth('POST')
@check_headers_version
def remove(request):
    password = request.POST.get('password', None)
    if password is None:
        raise Http404
    if not request.user.check_password(password):
        return auth_error
    request.user.is_active = False
    request.user.save()
    user_profile = request.user.get_profile()
    user_profile.profile_image = ''
    user_profile.gender = ''
    user_profile.country = ''
    user_profile.city = ''
    user_profile.birthday = None
    user_profile.height = 0
    user_profile.weight = 0
    user_profile.blood = 0
    user_profile.save()
    auth_logout(request)
    return status_ok
