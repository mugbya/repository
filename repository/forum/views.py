from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.generic import ListView, View, TemplateView


class IndexView(TemplateView):
    template_name = 'forum/index.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        pass

