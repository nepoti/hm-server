from django.http import Http404, QueryDict
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from response.templates import auth_error, status_ok, ok_response, invalid_data, task_error
from response.decorators import check_method_auth, check_methods_auth
from user.models import UserProfile
from social.models import UploadUrl
from boto import s3
from hashlib import sha256
from os import urandom

max_size = 5*1024*1024


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
    user_profile = UserProfile.objects.filter(user_id=request.user.id)[0]
    user_profile.profile_image = ''
    user_profile.gender = ''
    user_profile.country = ''
    user_profile.city = ''
    user_profile.birthday = None
    user_profile.about = ''
    user_profile.achievements = '{}'
    for follower in user_profile.followers:
        obj = UserProfile.objects.filter(id=follower)[0]
        if user_profile.id in obj.following:
            obj.following.remove(user_profile.id)
    for following in user_profile.following:
        obj = UserProfile.objects.filter(id=following)[0]
        if user_profile.id in obj.followers:
            obj.followers.remove(user_profile.id)
    user_profile.followers = []
    user_profile.following = []
    user_profile.save()
    auth_logout(request)
    return status_ok


@csrf_exempt
@check_method_auth('POST')
def get_posts(request):
    user_id = request.POST.get('id', None)
    page = request.POST.get('page', 0)
    limit = request.POST.get('limit', 10)
    try:
        page = int(page)
        limit = int(limit)
        if page < 0 or limit < 0:
            return invalid_data
        if limit > 10:
            limit = 10
        if user_id:
            return UserProfile.objects.filter(id=int(user_id))[0].get_posts(page, limit)
        else:
            return UserProfile.objects.filter(user_id=request.user.id)[0].get_posts(page, limit)
    except:
        return invalid_data


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
        user_id = request.POST.get('id', None)
        page = request.POST.get('page', 0)
        try:
            page = int(page)
            if page < 0:
                return invalid_data
            if user_id:
                return UserProfile.objects.filter(id=int(user_id))[0].get_followers(page)
            else:
                return UserProfile.objects.filter(user_id=request.user.id)[0].get_followers(page)
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
    user_id = request.POST.get('id', None)
    page = request.POST.get('page', 0)
    try:
        page = int(page)
        if page < 0:
                return invalid_data
        if user_id:
            return UserProfile.objects.filter(id=int(user_id))[0].get_following(page)
        else:
            return UserProfile.objects.filter(user_id=request.user.id)[0].get_following(page)
    except:
        return invalid_data


client = s3.connect_to_region('eu-central-1', host='s3.eu-central-1.amazonaws.com')


def new_upload_url(length):
    try:
        exists = True
        i = 0
        while exists:
            key = sha256(urandom(32).encode('base_64')).hexdigest()
            exists = UploadUrl.objects.filter(key=key).exists()
            i += 1
            if i == 10:
                return None
        return [key,
                client.generate_url_sigv4(3600, 'PUT', 'thehealthme', key + '.jpg',
                                          headers={'Content-Type': 'image/jpeg', 'Content-Length': length})]
    except:
        return [None, None]


@csrf_exempt
@check_method_auth('POST')
def imgupload(request):
    try:
        length = int(request.POST.get('length', None))
    except:
        return invalid_data
    if length > max_size:
        return invalid_data
    key, url = new_upload_url(length)
    if url:
        obj = UploadUrl(key=key)
        obj.save()
        return ok_response([url])
    else:
        return task_error
