from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^login/$', 'accounts.views.login_endpoint', name='login_endpoint'),
    url(r'^me/$', 'accounts.views.me_endpoint', name='me_endpoint'),
    url(r'^logout/$', 'accounts.views.logout_endpoint', name='logout_endpoint'),
]
