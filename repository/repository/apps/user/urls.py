# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import logout_then_login
from .views import RegisterView, LoginForm

urlpatterns = [

    url(r'^login/$', LoginForm.as_view(), name='login'),

    url(r'^logout/$', logout_then_login, name="logout"),

    url(r'^register/$', RegisterView.as_view(), name='register'),

]





