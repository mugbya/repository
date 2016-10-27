# -*- coding: utf-8 -*-
from django.conf.urls import url

from django.contrib.auth.views import logout_then_login, password_change
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^quiz/$', views.CreateView.as_view(), name='quiz'),
    url(r'^(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/$', views.DetailView.as_view(), name='detail'),


]
