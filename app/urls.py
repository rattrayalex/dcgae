from django.conf.urls.defaults import *
from app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^rank/(.+)/$', rank), 
##    (r'^choices/(.+)/$', choices), 
##    (r'^choose/$', choose), #maybe keep this one for later.
    (r'^thanks/(.+)/$', thanks), 
    (r'^results/(.+)/$', results), 
    (r'^signin/$', signin),
    (r'^signup/$', signup),
    (r'^$', index), 
    (r'^loggedin/$', loggedin),
    (r'^logout/$', logout),
    (r'^upload/$', upload_files),
    (r'vote/$', vote),
    (r'^img_uploader/$', myFileHandler),
    (r'image_handler/(.+)/(.+)/(.+)$', image_handler),
    )
