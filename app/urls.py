###########################################################################
## \file app/ulrs.py
## \brief Defines the allowed urls of the webapp
## \author mrudelle@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################

from django.conf.urls.defaults import *
from django.contrib import admin
import views 
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()


urlpatterns = patterns('',

    # Used by Django to start the web app
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),

    # Various pages that can be requested
    url(r'^$', 'views.index', name='index'),
    url(r'^about/$', 'views.about', name='about'),
    url(r'^faq/$', 'views.faq', name='faq'),
    url(r'^app/$', 'views.app', name='app'),
    url(r'^settings/$', 'views.settings', name='settings'),

    # Various pagelet of the app page that can be requested 
    url(r'^app/file=(?P<file>.+)$', 'views.file_page', name='pagelet_file'),
    url(r'^app/file_list/$', 'views.file_list', name='pagelet_list'),

    # Used for administration purpose
    ('^admin/', include(admin.site.urls))
)
