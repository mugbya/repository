# -*- coding: utf-8 -*-
__author__ = 'mugbya'

from django.http import HttpResponse

def hello(request):
    return HttpResponse("欢迎进入知识库系统！")