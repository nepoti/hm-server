from django.http import Http404
from django.contrib.auth import logout as auth_logout
from response.templates import auth_error, status_ok, ok_response, invalid_data, task_error
from response.decorators import check_method_auth, check_headers_version
from user.models import UserProfile, Follow


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
    user_profile = UserProfile.objects.filter(user_id=request.user.id)[0]
    user_profile.profile_image = ''
    user_profile.gender = ''
    user_profile.country = ''
    user_profile.city = ''
    user_profile.birthday = None
    user_profile.about = ''
    user_profile.achievements = '{}'
    Follow.objects.filter(following=user_profile).delete()
    Follow.objects.filter(follower=user_profile).delete()
    user_profile.save()
    auth_logout(request)
    return status_ok
