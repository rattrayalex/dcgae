# below came from http://stackoverflow.com/questions/1348669/uploading-multiple-files-with-django/1736273#1736273
class FakeUploadCookieMiddleware(object):
   """TODO: replace the hardcoded url '/upload' with a 'reverse'."""
   def process_request(self, request):
       if request.path == '/upload/' \
           and request.POST.has_key(settings.SESSION_COOKIE_NAME):
           request.COOKIES[settings.SESSION_COOKIE_NAME] = \
               request.POST[settings.SESSION_COOKIE_NAME]
           logging.debug('Faking the session cookie for an upload: %s', \
               request.POST[settings.SESSION_COOKIE_NAME])

# below came from http://stackoverflow.com/questions/1348669/uploading-multiple-files-with-django/1736273#1736273
class FakeUploadCookieMiddleware(object):
   """TODO: replace the hardcoded url '/upload' with a 'reverse'."""
   def process_request(self, request):
       if request.path == '/upload/' \
           and request.POST.has_key(settings.SESSION_COOKIE_NAME):
           request.COOKIES[settings.SESSION_COOKIE_NAME] = \
               request.POST[settings.SESSION_COOKIE_NAME]
           logging.debug('Faking the session cookie for an upload: %s', \
               request.POST[settings.SESSION_COOKIE_NAME])
