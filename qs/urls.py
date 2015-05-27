# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.sitemaps import GenericSitemap
# from django.contrib.sitemaps.views import sitemap

from . import models
from . import views
# from . import rss


urlpatterns = [
    #网站首页
    url(r'^$', views.IndexView.as_view(), name='index'),

]

