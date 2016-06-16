"""repository URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

# admin.autodiscover()

urlpatterns = [
    # 别多加$
    url(r'^', include('qs.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^oauth/', include('oauth.urls')),

    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url('', include('django.contrib.auth.urls')),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
