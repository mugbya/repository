# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    # 这里竟然还有顺序.....
    url(r'^register$', views.register, name='register'),

    url(r'^settings$', views.settings, name='settings'),

    url(r'^(?P<username>[A-Za-z0-9]+)$', views.index, name='user_index'),



    url(r'^avatar$', views.avatar, name='avatar'),

]





