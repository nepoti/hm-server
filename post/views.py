from django.http import Http404
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from response.decorators import check_method_auth, check_methods_auth
from response.templates import invalid_data
from social.models import Post
from user.models import UserProfile
from json import loads


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
def proceed(request):
    author = UserProfile.objects.filter(user_id=request.user.id)[0]
    if request.method == 'POST':
        id = request.POST.get('id', None)
        data = request.POST.get('data', None)
        if data:
            try:
                data = loads(data)
            except:
                return invalid_data
        else:
            return invalid_data
        text = data.get('text', None) or None
        photos = data.get('photos', None) or None
        locations = data.get('locations', None) or None
        if id:
            try:
                post = Post.objects.filter(id=id)[0]
            except:
                return invalid_data
            return post.edit(author, text, photos, locations)
        return Post.create(author, text, photos, locations)
    else:  # DELETE
        id = QueryDict(request.body).get('id', None)
        if id is None:
            raise Http404
        try:
            post = Post.objects.filter(id=id)[0]
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
