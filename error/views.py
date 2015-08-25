from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from models import Error
from response.templates import status_ok


@csrf_exempt
def error(request):
    if request.method != 'POST':
        raise Http404
    msg = request.POST.get('error', None)
    if msg is None:
        raise Http404
    Error(message=msg).save()
    return status_ok