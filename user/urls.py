# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),

    url(r'^settings$', views.settings, name='settings'),

    url(r'^avatar$', views.avatar, name='avatar'),

    url(r'^(?P<username>[A-Za-z0-9\_]+)$', views.index, name='user_index'),
]





