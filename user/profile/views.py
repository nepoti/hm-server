from django.http import Http404
from response.templates import invalid_data
from response.decorators import check_methods_auth, check_headers_version
from json import loads
from django.views.decorators.gzip import gzip_page


def read(request):
    return request.user.userprofile.get_info()


def update(request):
    data = request.POST.get('data', None)
    if data is None:
        raise Http404
    try:
        data = loads(data)
    except:
        return invalid_data
    return request.user.userprofile.set_info(data)


@check_methods_auth(['GET', 'POST'])
@check_headers_version
@gzip_page
def profile(request):
    if request.method == 'GET':
        return read(request)
    elif request.method == 'POST':
        return update(request)
    else:
        raise Http404