from django.conf.urls.defaults import *
from django.contrib import admin
import views #TODO may need to be moved, to be decided later
import dbindexer
import API.PALUsers as auth

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    #('^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    url(r'^$', 'views.index', name='index'),
    url(r'^about/$', 'views.about', name='about'),
    url(r'^faq/$', 'views.faq', name='faq'),
    url(r'^app/$', 'views.app', name='app'),
    url(r'^app/(?P<file>.+)$', 'views.app', name='app'),
    url(r'^settings/$', 'views.settings', name='settings'),
	url(r'^login/$', 'views.login', name='login'),
	url(r'^logout/$', 'views.logout', name='logout'),
    ('^admin/', include(admin.site.urls))
)
