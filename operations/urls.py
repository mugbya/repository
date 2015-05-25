__author__ = 'mugbya'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'operations.views.index'),
                       url(r'^list$', 'operations.views.list'),
                       url(r'^test$', 'operations.views.test'),
                       )
