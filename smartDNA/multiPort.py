from django.conf import settings
 
 
class MultiPortMiddleware(object):
    def process_request(self, request):
	settings.SESSION_COOKIE_NAME = 'sessionid' + request.META['SERVER_PORT']
	return None 
