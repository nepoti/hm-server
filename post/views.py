from django.http import Http404
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from response.decorators import check_methods_auth
from response.templates import invalid_data
from social.models import Post
from user.models import UserProfile


@csrf_exempt
@check_methods_auth(['POST', 'DELETE'])
def proceed(request):
    author = UserProfile.objects.filter(user_id=request.user.id)[0]
    if request.type == 'POST':
        id = request.POST.get('id', None)
        text = request.POST.get('text', None)
        photos = request.POST.get('photos', None)
        locations = request.POST.get('locations', None)
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
