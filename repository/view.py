# -*- coding: utf-8 -*-
__author__ = 'mugbya'

# from django.http import HttpResponse
from django.shortcuts import render
# from django.core.context_processors import csrf


def index(request):
    return render(request, 'repository/index.html', {})