# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import GithubView

urlpatterns = [

    url(r'^github/$', GithubView.as_view(), name='github'),



]