from django.conf.urls import include, url
from django.contrib import admin
from accounts.views import me_endpoint
urlpatterns = [
    # Examples:
    # url(r'^$', 'dragonfly.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', me_endpoint),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
]
