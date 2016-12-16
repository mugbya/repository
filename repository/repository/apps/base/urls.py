# -*- coding: utf-8 -*-
from django.conf.urls import url

from django.contrib.auth.views import logout_then_login, password_change
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),


]
