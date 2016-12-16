# -*- coding: utf-8 -*-
from django.views import generic
from blog.models import Blog


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        blogs = Blog.objects.all()
        return blogs