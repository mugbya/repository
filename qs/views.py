# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, FormView, TemplateView
from django.contrib.auth import authenticate, login
from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput
from django.utils.six import BytesIO

from .models import *

class IndexView(TemplateView):
    template_name = 'qs/index.html'

    def get_context_data(self, **kwargs):
        list = Qs.objects.all()
        # 这里和下面的headline那里加的这个判断是为了空数据库的时候出现IndexError
        # admin_post = list.filter(bygod=1) or [None, ]
        return {
            'post_latest': list[:10],
        }

