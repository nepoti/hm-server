from django.http import Http404, QueryDict
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from response.templates import auth_error, status_ok, ok_response, invalid_data, task_error
from response.decorators import check_method_auth, check_methods_auth, check_headers_version
from user.models import UserProfile, Follow
from social.models import UploadUrl
from boto import s3
from hashlib import sha256
from os import urandom
import constants as c


@csrf_exempt
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


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
def get_posts(request):
    user_id = request.POST.get('id', None)
    offset = request.POST.get('offset', 0)
    limit = request.POST.get('limit', c.REQUEST_MAX_POSTS)
    try:
        offset = int(offset)
        limit = int(limit)
        if offset < 0 or limit < 1:
            return invalid_data
        if limit > c.REQUEST_MAX_POSTS:
            limit = c.REQUEST_MAX_POSTS
        if user_id:
            return UserProfile.objects.filter(id=int(user_id))[0].get_posts(offset, limit)
        else:
            return UserProfile.objects.filter(user_id=request.user.id)[0].get_posts(offset, limit)
    except:
        return invalid_data


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
@check_headers_version
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
@check_headers_version
def followers(request):
    if request.method == 'POST':
        user_id = request.POST.get('id', None)
        offset = request.POST.get('offset', 0)
        limit = request.POST.get('limit', c.REQUEST_MAX_FOLLOWERS)
        try:
            offset = int(offset)
            limit = int(limit)
            if offset < 0 or limit < 1:
                return invalid_data
            if limit > c.REQUEST_MAX_FOLLOWERS:
                limit = c.REQUEST_MAX_FOLLOWERS
            if user_id:
                return UserProfile.objects.filter(id=int(user_id))[0].get_followers(offset, limit)
            else:
                return UserProfile.objects.filter(user_id=request.user.id)[0].get_followers(offset, limit)
        except:
            return invalid_data
    else:  # DELETE
        follower_id = QueryDict(request.body).get('id', None)
        if follower_id is None:
            raise Http404
        return UserProfile.objects.filter(user_id=request.user.id)[0].follower_remove(follower_id)


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
def following(request):
    user_id = request.POST.get('id', None)
    offset = request.POST.get('offset', 0)
    limit = request.POST.get('limit', c.REQUEST_MAX_FOLLOWING)
    try:
        offset = int(offset)
        limit = int(limit)
        if offset < 0 or limit < 1:
            return invalid_data
        if limit > c.REQUEST_MAX_FOLLOWING:
            limit = c.REQUEST_MAX_FOLLOWING
        if user_id:
            return UserProfile.objects.filter(id=int(user_id))[0].get_following(offset, limit)
        else:
            return UserProfile.objects.filter(user_id=request.user.id)[0].get_following(offset, limit)
    except:
        return invalid_data


client = s3.connect_to_region(c.S3_REGION, host=c.S3_HOST)


def new_upload_url(length):
    try:
        exists = True
        i = 0
        while exists:
            key = sha256(urandom(32).encode('base_64')).hexdigest()
            exists = UploadUrl.objects.filter(key=key).exists()
            i += 1
            if i == c.S3_MAX_URL_GENERATE_ATTEMPTS:
                return None
        return [key,
                client.generate_url_sigv4(c.S3_URL_EXPIRATION_TIME, 'PUT', c.S3_BUCKET, key + '.jpg',
                                          headers={'Content-Type': 'image/jpeg', 'Content-Length': length})]
    except:
        return [None, None]


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
def imgupload(request):
    length = request.POST.get('length', None)
    if length is None:
        raise Http404
    try:
        length = int(length)
    except:
        return invalid_data
    if length < 1 or length > c.S3_MAX_FILE_SIZE:
        return invalid_data
    key, url = new_upload_url(length)
    if url:
        obj = UploadUrl(key=key)
        obj.save()
        return ok_response([url])
    else:
        return task_error
