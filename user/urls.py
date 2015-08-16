# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from .views import RegisterView, BindView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),

    url(r'^bind', BindView.as_view(), name='bind'),

    url(r'^settings$', views.settings, name='settings'),

    url(r'^resetpwd$', views.resetpwd, name='resetpwd'),

    url(r'^uploadavatar_upload$', views.uploadavatar_upload, name='uploadavatar_upload'),

    url(r'^(?P<username>[A-Za-z0-9\_]+)$', views.userIndex, name='user_index'),
]





