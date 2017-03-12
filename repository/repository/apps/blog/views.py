# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator

from django.views import generic
from .models import Blog
from .forms import BlogForm


@method_decorator(login_required, name='dispatch')
class CreateView(generic.CreateView):
    template_name = 'blog/add.html'
    form_class = BlogForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        tags = form.data.get('tags', None)
        if tags:
            tag_list = tags.spilt(',')
            for tag in tag_list:
                pass


        return super(CreateView, self).form_valid(form)


class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        context['object'] = self.object
        return context


@method_decorator(login_required, name='dispatch')
class UpdateView(generic.UpdateView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    model = Blog

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super(UpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteView(generic.DeleteView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse('blog:detail', args=(self.object.id,))

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        obj.is_active = False
        obj.save()
        return obj
