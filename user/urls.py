# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from .views import RegisterView, BindNewUserView, BindView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),

    url(r'^confirm/(?P<token>[0-9A-Za-z]{19})$', views.bindConfirm, name='bind_confirm'),

    url(r'^bind$', BindView.as_view(), name='bind'),

    url(r'^bindnew$', BindNewUserView.as_view(), name='bind_new'),

    url(r'^settings$', views.settings, name='settings'),

    url(r'^resetpwd$', views.resetpwd, name='resetpwd'),

    url(r'^uploadavatar_upload$', views.uploadavatar_upload, name='uploadavatar_upload'),

    url(r'^(?P<username>[A-Za-z0-9\_]+)$', views.userIndex, name='user_index'),
]





