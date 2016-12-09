# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import logout_then_login
from .views import RegisterView, LoginForm, password_reset_confirm, password_reset_complete, password_reset

urlpatterns = [

    url(r'^login/$', LoginForm.as_view(), name='login'),

    url(r'^logout/$', logout_then_login, name="logout"),

    url(r'^register/$', RegisterView.as_view(), name='register'),

    # url(r'^bindnew$', BindNewUserView.as_view(), name='bind_new'),

    # url(r'^bind$', BindView.as_view(), name='bind'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, name='password_reset_confirm'),
    # url(r'^resetpwd$', ResetPWD.as_view(), name='reset_pwd'),

    # url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset, name='password_reset'),
]
