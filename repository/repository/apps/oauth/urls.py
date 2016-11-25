# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import GitHubView, GitHubVerifyView

urlpatterns = [

    url(r'^github/$', GitHubView.as_view(), name='github'),
    url(r'^github/verify/$', GitHubVerifyView.as_view(), name='github_verify'),



]