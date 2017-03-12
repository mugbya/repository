# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^quiz/$', views.CreateView.as_view(), name='quiz'),
    url(r'^(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/edit/$', views.UpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})/del/$', views.DeleteView.as_view(), name='del'),

]
