# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})$', views.DetailView.as_view(), name='detail'),


    # url(r'^new$', views.new_blog, name='new_blog'),
    url(r'^new$', views.CreateView.as_view(), name='new_blog'),

    # # url(r'^settings$', views.settings, name='settings'),
    # #
    # # url(r'^uploadavatar_upload$', views.uploadavatar_upload, name='uploadavatar_upload'),
    #
    # url(r'^blog/(?P<username>[A-Za-z0-9\_]+)$', views.blogs, name='user_blog'),
]



