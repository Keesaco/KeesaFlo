from django.conf.urls.defaults import *
from django.contrib import admin
import views #TODO may need to be moved, to be decided later
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    #('^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    url(r'^$', 'views.index', name='index'),
    url(r'^app/panels/main/about/$', 'views.about', name='about'),
    url(r'^app/panels/main/faq/$', 'views.faq', name='faq'),
    url(r'^app/$', 'views.app', name='app'),
    url(r'^app/panels/main/file=(?P<file>.+)$', 'views.file_preview', name='pagelet_file'),
    url(r'^app/panels/right/file_list/$', 'views.file_list', name='pagelet_list'),
	url(r'^app/panels/left/toolselect/$', 'views.toolselect', name='toolselect'),
	url(r'^app/panels/left/pagenav/$', 'views.pagenav', name='pagenav'),
    url(r'^app/settings/$', 'views.settings', name='settings'),
    ('^admin/', include(admin.site.urls))
)
