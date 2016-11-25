# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import logout_then_login
from .views import RegisterView, LoginForm, ResetPWD

urlpatterns = [

    url(r'^login/$', LoginForm.as_view(), name='login'),

    url(r'^logout/$', logout_then_login, name="logout"),

    url(r'^register/$', RegisterView.as_view(), name='register'),

    # url(r'^bindnew$', BindNewUserView.as_view(), name='bind_new'),

    # url(r'^bind$', BindView.as_view(), name='bind'),

    url(r'^resetpwd$', ResetPWD.as_view(), name='reset_pwd'),
]
