from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^signup/$', 'accounts.views.signup_endpoint', name='signup_endpoint'),
    url(r'^login/$', 'accounts.views.login_endpoint', name='login_endpoint'),
    url(r'^me/$', 'accounts.views.me_endpoint', name='me_endpoint'),
    url(r'^logout/$', 'accounts.views.logout_endpoint', name='logout_endpoint'),
    url(r'^recovery/$', 'accounts.views.recovery_endpoint', name='recovery_endpoint'),
    url(r'^recovery/form/$', 'accounts.views.recovery_form_endpoint', name='recovery_form_endpoint'),
]
