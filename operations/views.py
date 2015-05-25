# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
#
#  http://zhaofei.tk/2014/12/26/django_start/#comment-1786960623
#  http://djangobook.py3k.cn/2.0/chapter01/
#   http://www.w3cschool.cc/django/django-template.html
#
#   https://github.com/Vamei/Python-Tutorial-Vamei/blob/master/content%2F%E8%A2%AB%E8%A7%A3%E6%94%BE%E7%9A%84%E5%A7%9C%E6%88%8802%20%E5%BA%84%E5%9B%AD%E7%96%91%E4%BA%91.md
#

#  archlinux percona  安装

#  模板的详解
#  http://www.cnblogs.com/btchenguang/archive/2012/09/05/2672364.html


# from django.http import HttpResponse
from operations.models import Classification

# def index(request):
#     return HttpResponse("欢迎进入运维知识库！")
#
def list(request):
    list = Classification.objects.all()
    # print(list + " : " + list.type)
    list_str = map(str, list)
    # return HttpResponse("<p>" + ' '.join(list_str) + "</p>")
    context = {'label': ' '.join(list_str)}
    return render(request, 'templay.html', context)

def test(request):
    context = {}
    context['label'] = 'Hello World!'
    return render(request, 'templay.html', context)  #

