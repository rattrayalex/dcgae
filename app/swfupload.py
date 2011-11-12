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

from django.conf import settings
from django.core.urlresolvers import reverse
import logging

class SWFUploadMiddleware(object):
    def process_request(self, request):
        logging.warning("in swfuploadmiddlware thing")
        if (request.method == 'POST') and (request.path == reverse('app.views.myFileHandler')) and \
                request.POST.has_key(settings.SESSION_COOKIE_NAME):
            logging.warning("if statement true")
            request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]

class take3():
    def process_request(self, request):
        if (request.method == 'POST'):
           if request.POST.has_key('biscuit'):
              biscuit = request.POST['biscuit']
              for i in biscuit.split(" "):
                x, y = i.split('=')
                request.COOKIES[x.strip('; ')] = y.strip('; ')
