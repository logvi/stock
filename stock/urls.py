from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^stock/', include('apps.AppStock.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Authenticate
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html'},  name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/stock/'}, name='logout'),
)
