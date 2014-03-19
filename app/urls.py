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
import API.PALUsers as auth

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
    url(r'^app/panels/main/about/$', 'views.about', name='about'),
    url(r'^app/panels/main/faq/$', 'views.faq', name='faq'),
    url(r'^app/$', 'views.app', name='app'),
    url(r'^app/panels/main/file=(?P<file>.+)$', 'views.file_preview', name='pagelet_file'),
    url(r'^app/panels/main/fetch_graph=(?P<graph>.+)\.png$', 'views.get_graph', name='get_graph'),
    url(r'^app/panels/main/fetch_dataset=(?P<dataset>.+)$', 'views.get_dataset', name='get_dataset'),
    url(r'^app/panels/right/file_list/$', 'views.file_list', name='pagelet_list'),
	url(r'^app/panels/left/toolselect/$', 'views.toolselect', name='toolselect'),
	url(r'^app/panels/left/pagenav/$', 'views.pagenav', name='pagenav'),
    url(r'^app/gating/rectangular/(?P<params>[\.,-_ \d\w()]+)$', 'views.rect_gating', name='gating_rect'),
    url(r'^app/gating/polygon/(?P<params>[\.,-_ \d\w()]+)$', 'views.poly_gating', name='gating_poly'),
    url(r'^app/gating/oval/(?P<params>[\.,-_ \d\w()]+)$', 'views.oval_gating', name='gating_oval'),
	url(r'^login/$', 'views.login', name='login'),
	url(r'^logout/$', 'views.logout', name='logout'),
    url(r'^settings/$', 'views.settings', name='settings'),

    # Used for administration purpose5
    ('^admin/', include(admin.site.urls))
)
