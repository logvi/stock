__author__ = 'vitalijlogvinenko'
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.AppStock import views

urlpatterns = patterns('',
    url(r'^$', views.index, {'cat_id':1, 'page':1}, name="index" ),
    url(r'^(?P<cat_id>\d+)/(?P<page>\d+)/$', views.index, name="index" ),
    url(r'^parsing/', views.parsing, name="parsing" ),
    url(r'^$', views.index, name="index" ),
    url(r'^upload/$', views.upload, {'per':'D','cat_id':1}, name="upload" ),
    url(r'^upload/(?P<cat_id>\d+)/(?P<per>\w+)/$', views.upload, name="upload_per" ),
    url(r'^admin/', include(admin.site.urls)),
)