from django.http import Http404
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from response.decorators import check_method_auth, check_methods_auth
from response.templates import invalid_data
from social.models import Post
from social.models import PostComment
from user.models import UserProfile
from json import loads


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
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
def get_post(request):
    post_id = request.POST.get('id', None)
    if post_id is None:
        raise Http404
    return Post.get_post(post_id)


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
def like_post(request):
    post_id = QueryDict(request.body).get('id', None)
    if post_id is None:
        raise Http404
    return Post.like_post(post_id, UserProfile.objects.filter(user_id=request.user.id)[0], request.method == 'POST')


@csrf_exempt
@check_method_auth('POST')
def get_likes(request):
    post_id = request.POST.get('id', None)
    page = request.POST.get('page', 0)
    try:
        post_id = int(post_id)
        page = int(page)
        return Post.get_likes(post_id, page)
    except:
        return invalid_data


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
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
def get_comment(request):
    comment_id = request.POST.get('id', None)
    if comment_id is None:
        raise Http404
    return PostComment.get_comment(comment_id)
