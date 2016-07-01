from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.decorators import method_decorator

from .models import Blog
from .forms import BlogForm
from repository.settings import PAGE_NUM


class IndexView(generic.ListView):
    '''
    all blog list
    '''
    paginate_by = PAGE_NUM
    template_name = 'blog/index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        object_list = Blog.objects.filter(published_date__isnull=False, is_active=True).order_by('-published_date')[:100]
        return object_list


class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context


# 1.9 可以有如下写法 api: https://docs.djangoproject.com/en/1.9/topics/class-based-views/intro/#decorating-the-class
@method_decorator(login_required, name='dispatch')
class CreateView(generic.CreateView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    # success_url = '/blog/'

    def get_success_url(self):
        return reverse('blog:detail', args=(self.object.id,))

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if 'publish' in self.request.POST:
            post.publish()
        else:
            post.save()
            return redirect('blog:private')
        return super(CreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdateView(generic.UpdateView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    model = Blog

    def get_success_url(self):
        return reverse('blog:detail', args=(self.object.id,))

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if 'publish' in self.request.POST:
            post.publish()
        else:
            post.save()
            return redirect('blog:private')
        return super(UpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteView(generic.DeleteView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        obj.is_active = False
        obj.save()
        return obj

