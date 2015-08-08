from django.http import Http404
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from response.decorators import check_method_auth, check_methods_auth, check_headers_version
from response.templates import invalid_data
from social.models import Post
from social.models import PostComment
from user.models import UserProfile
from json import loads
import constants as c
from django.views.decorators.gzip import gzip_page


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
@check_headers_version
def proceed_post(request):
    author = UserProfile.objects.filter(user_id=request.user.id)[0]
    if request.method == 'POST':
        post_id = request.POST.get('id', None)
        data = request.POST.get('data', None)
        if data is not None:
            try:
                data = loads(data)
            except:
                return invalid_data
        else:
            return invalid_data
        text = data.get('text', None) or None
        photos = data.get('photos', None) or None
        locations = data.get('locations', None) or None
        if post_id is not None:
            try:
                post = Post.objects.filter(id=post_id)[0]
            except:
                return invalid_data
            return post.edit(author, text, photos, locations)
        return Post.create(author, text, photos, locations)
    else:  # DELETE
        post_id = QueryDict(request.body).get('id', None)
        if post_id is None:
            raise Http404
        try:
            post = Post.objects.filter(id=post_id)[0]
        except:
            return invalid_data
        return post.remove(author)


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
@gzip_page
def get_post(request):
    post_id = request.POST.get('id', None)
    if post_id is None:
        raise Http404
    return Post.get_post(post_id)


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
@check_headers_version
def like_post(request):
    post_id = QueryDict(request.body).get('id', None)
    if post_id is None:
        raise Http404
    return Post.like_post(post_id, UserProfile.objects.filter(user_id=request.user.id)[0], request.method == 'POST')


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
@gzip_page
def get_likes(request):
    post_id = request.POST.get('id', None)
    offset = request.POST.get('offset', 0)
    limit = request.POST.get('limit', c.REQUEST_MAX_LIKES)
    try:
        post_id = int(post_id)
        offset = int(offset)
        limit = int(limit)
        if offset < 0 or limit < 1:
            return invalid_data
        if limit > c.REQUEST_MAX_LIKES:
            limit = c.REQUEST_MAX_LIKES
        return Post.get_likes(post_id, offset, limit)
    except:
        return invalid_data


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
@check_headers_version
def proceed_comment(request):
    author = UserProfile.objects.filter(user_id=request.user.id)[0]
    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        comment_id = request.POST.get('id', None)
        data = request.POST.get('data', None)
        if data is not None:
            try:
                data = loads(data)
            except:
                return invalid_data
        else:
            return invalid_data
        text = data.get('text', None) or None
        photos = data.get('photos', None) or None
        locations = data.get('locations', None) or None
        if comment_id is not None:
            try:
                comment = PostComment.objects.filter(id=comment_id)[0]
            except:
                return invalid_data
            return comment.edit(author, text, photos, locations)
        if post_id is not None:
            try:
                post = Post.objects.filter(id=post_id)[0]
            except:
                return invalid_data
            return PostComment.create(post, author, text, photos, locations)
        return invalid_data
    else:  # DELETE
        comment_id = QueryDict(request.body).get('id', None)
        if comment_id is None:
            raise Http404
        try:
            comment = PostComment.objects.filter(id=comment_id)[0]
        except:
            return invalid_data
        return comment.remove(author)


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
@gzip_page
def get_comment(request):
    comment_id = request.POST.get('id', None)
    if comment_id is None:
        raise Http404
    return PostComment.get_comment(comment_id)


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
@gzip_page
def get_comments(request):
    post_id = request.POST.get('id', None)
    offset = request.POST.get('offset', 0)
    limit = request.POST.get('limit', c.REQUEST_MAX_COMMENTS)
    try:
        post_id = int(post_id)
        offset = int(offset)
        limit = int(limit)
        if offset < 0 or limit < 1:
            return invalid_data
        if limit > c.REQUEST_MAX_COMMENTS:
            limit = c.REQUEST_MAX_COMMENTS
        return Post.get_comments(post_id, offset, limit)
    except:
        return invalid_data


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
@check_headers_version
def like_comment(request):
    comment_id = QueryDict(request.body).get('id', None)
    if comment_id is None:
        raise Http404
    return PostComment.like_comment(comment_id,
                                    UserProfile.objects.filter(user_id=request.user.id)[0], request.method == 'POST')


@csrf_exempt
@check_method_auth('POST')
@check_headers_version
@gzip_page
def get_comment_likes(request):
    comment_id = request.POST.get('id', None)
    offset = request.POST.get('offset', 0)
    limit = request.POST.get('limit', c.REQUEST_MAX_LIKES)
    try:
        comment_id = int(comment_id)
        offset = int(offset)
        limit = int(limit)
        if offset < 0 or limit < 1:
            return invalid_data
        if limit > c.REQUEST_MAX_LIKES:
            limit = c.REQUEST_MAX_LIKES
        return PostComment.get_likes(comment_id, offset, limit)
    except:
        return invalid_data
