# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator

from django.views import generic
from .models import Blog
from .forms import BlogForm


@method_decorator(login_required, name='dispatch')
class CreateView(generic.CreateView):
    template_name = 'blog/edit.html'
    # template_name = 'forum/tmp/edit.html'
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blog:detail', args=(self.object.id,))

    def form_valid(self, form):
        post = form.save(commit=False)
        # post.author = self.request.user
        post.save()

        return super(CreateView, self).form_valid(form)


class DetailViewOO(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailViewOO, self).get_context_data(**kwargs)
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