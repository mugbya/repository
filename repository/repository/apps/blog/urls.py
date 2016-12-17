# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^quiz/$', views.CreateView.as_view(), name='quiz'),
    url(r'^(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/$', views.DetailViewOO.as_view(), name='detail'),


]
