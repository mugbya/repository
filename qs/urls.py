# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.sitemaps import GenericSitemap
# from django.contrib.sitemaps.views import sitemap

from . import views
# from . import rss


urlpatterns = [
    #网站首页
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^qs/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^qs/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'), edit_solution
    # url(r'^qs/new/$', views.CreateView.as_view(), name='new_qs'),
    url(r'^qs/new/$', views.new_qs, name='new_qs'),
    url(r'^qs/(?P<pk>[0-9]+)/edit/$', views.edit_qs, name='edit_qs'),
    url(r'^qs/(?P<pk>[0-9]+)/del_qs/$', views.del_qs, name='del_qs'),
    url(r'^qs/(?P<pk>[0-9]+)/edit_solution/$', views.edit_solution, name='edit_solution'),
    url(r'^qs/(?P<pk>[0-9]+)/del_solution/$', views.del_solution, name='del_solution'),
    # url(r'^qs/(?P<pk>[0-9]+)/save_solution/$', views.save_solution, name='save_solution'),



    url(r'^qs/reply', views.reply, name='reply'),
    url(r'^user/draft/$', views.draft, name='draft'),


    url(r'^accounts/register/$', views.register, name='register'),

]

