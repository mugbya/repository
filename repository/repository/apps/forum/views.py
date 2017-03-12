# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator

from django.views import generic
from .forms import QuestionForm
from .models import Question


class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        questions = Question.objects.all()
        return questions


@method_decorator(login_required, name='dispatch')
class CreateView(generic.CreateView):
    template_name = 'forum/edit.html'
    # template_name = 'forum/tmp/edit.html'
    form_class = QuestionForm

    def get_success_url(self):
        return reverse('forum:detail', args=(self.object.id,))

    def form_valid(self, form):
        post = form.save(commit=False)
        # post.author = self.request.user
        post.save()

        return super(CreateView, self).form_valid(form)

    def form_invalid(self, form):
        form
        return super(CreateView, self).form_invalid(form)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'forum/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # recommend_list = Recommend.objects.filter(blog=self.object, status=True)

        voted_status = '推荐'
        # if not self.request.user.is_anonymous():
        #     recommend = Recommend.objects.get_or_none(blog=self.object, user=self.request.user)
        #     if recommend and recommend.status:
        #         voted_status = '已推荐'

        # context['voted_status'] = voted_status
        # context['voted'] = len(recommend_list)
        context['object'] = self.object
        return context


@method_decorator(login_required, name='dispatch')
class UpdateView(generic.UpdateView):
    template_name = 'forum/edit.html'
    form_class = QuestionForm
    model = Question

    def get_success_url(self):
        return reverse('forum:detail', args=(self.object.id,))

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        # if 'publish' in self.request.POST:
        #     post.publish()
        # else:
        #     post.save()
        #     return redirect('blog:private')
        return super(UpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteView(generic.DeleteView):
    model = Question
    template_name = 'forum/detail.html'

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        # obj.is_active = False
        # obj.save()
        obj.delete()
        return redirect('base:index')