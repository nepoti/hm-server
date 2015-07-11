from django.http import Http404
from django.http import QueryDict
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from response.templates import auth_error
from response.templates import status_ok
from response.templates import ok_response
from response.templates import invalid_data
from response.decorators import check_method_auth, check_methods_auth
from user.models import UserProfile


@csrf_exempt
@check_method_auth('POST')
def remove(request):
    password = request.POST.get('password', None)
    if password is None:
        raise Http404
    if not request.user.check_password(password):
        return auth_error
    request.user.is_active = False
    request.user.save()
    auth_logout(request)
    return status_ok


@csrf_exempt
@check_method_auth('POST')
def get_posts(request):
    return ok_response(UserProfile.objects.filter(user_id=request.user.id)[0].get_posts())


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
def follow(request):
    if request.method == 'POST':
        follow_id = request.POST.get('id', None)
        if follow_id is None:
            raise Http404
        return UserProfile.objects.filter(user_id=request.user.id)[0].follow_add(follow_id)
    else:  # DELETE
        follow_id = QueryDict(request.body).get('id', None)
        if follow_id is None:
            raise Http404
        return UserProfile.objects.filter(user_id=request.user.id)[0].follow_remove(follow_id)


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
def followers(request):
    if request.method == 'POST':
        user_id = request.POST.get('id', None) or request.user.id
        page = request.POST.get('page', None) or 0
        try:
            user_id = int(user_id)
            page = int(page)
            return UserProfile.objects.filter(user_id=user_id)[0].get_followers(page)
        except:
            return invalid_data

    else:  # DELETE
        follower_id = QueryDict(request.body).get('id', None)
        if follower_id is None:
            raise Http404
        return UserProfile.objects.filter(user_id=request.user.id)[0].follower_remove(follower_id)

@csrf_exempt
@check_method_auth('POST')
def following(request):
    user_id = request.POST.get('id', None) or request.user.id
    page = request.POST.get('page', None) or 0
    try:
        user_id = int(user_id)
        page = int(page)
        return UserProfile.objects.filter(user_id=user_id)[0].get_following(page)
    except:
        return invalid_data
