# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.context_processors import csrf

# Create your views here.
#
#  http://zhaofei.tk/2015/01/11/django_start(2)/
#  http://djangobook.py3k.cn/2.0/chapter01/
#   http://www.w3cschool.cc/django/django-template.html
#

#  archlinux percona  安装

#  模板的详解
#  http://www.cnblogs.com/btchenguang/archive/2012/09/05/2672364.html


# from django.http import HttpResponse
from operations.models import Classification
from django import forms

def index(request):
    ctx = {}
    all_records = Classification.objects.all()
    ctx['list'] = all_records
    return render(request, "operations/index.html", ctx)

class ClassificationForm(forms.Form):
    name = forms.CharField(max_length=200)

def list(request):
    list = Classification.objects.all()
    return render(request, 'templay.html', {'list' : list})
    # list_str = map(str, list)
    # # return HttpResponse("<p>" + ' '.join(list_str) + "</p>")
    # context = {'label': ' '.join(list_str)}
    # return render(request, 'templay.html', context)

def test(request):
    context = {}
    context['label'] = 'Hello World!'
    return render(request, 'templay.html', context)  #

def addClassification(request):
    if request.POST:
        form = ClassificationForm(request.POST)
        if form.is_valid():
            submitted  = form.cleaned_data['name']
            new_record = Classification(name = submitted)
            new_record.save()
    form = ClassificationForm()
    ctx = {}
    ctx.update(csrf(request))
    all_records = Classification.objects.all()
    ctx['staff'] = all_records
    ctx['form'] = form
    return render(request, "addClassification.html", ctx)
    # if request.POST:
    #     submitted = request.POST['staff']
    #     new_record = Classification(name = submitted)
    #     new_record.save()
    # ctx ={}
    # ctx.update(csrf(request))
    # all_records = Classification.objects.all()
    # ctx['staff'] = all_records
    # return render(request, "addClassification.html", ctx)

