# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^qs/new$', views.new_qs, name='new_qs'),
    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})$', views.detail, name='detail'),
    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/edit$', views.edit_qs, name='edit_qs'),
    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/del_qs$', views.del_qs, name='del_qs'),
    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/edit_solution$', views.edit_solution, name='edit_solution'),
    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/del_solution$', views.del_solution, name='del_solution'),

    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/post_vote$', views.post_vote, name='post_vote'),

    url(r'^user/draft$', views.draft_list, name='draft_list'),
    url(r'^qs/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/draft$', views.draft_detail, name='draft_detail'),


    url(r'^search$', views.full_search, name='full_search')

]

