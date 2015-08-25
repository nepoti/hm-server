from time import time
from logging import getLogger


class LoggingMiddleware(object):
    def __init__(self):
        self.logger = getLogger('django.request')

    def process_request(self, request):
        request.timer = time()
        return None

    def process_response(self, request, response):
        self.logger.info(
            '[%s] %s (%.1fs) %s %s v%s',
            response.status_code,
            request.get_full_path(),
            time() - request.timer,
            request.META.get('HTTP_X_PLATFORM', 'Unknown platform'),
            request.META.get('HTTP_X_PLATFORM_VERSION', 'x.x'),
            request.META.get('HTTP_X_CLIENT_VERSION', 'x.x'),
        )
        return response
