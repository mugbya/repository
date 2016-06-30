from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
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
        object_list = Blog.objects.filter(published_date__isnull=False).order_by('-published_date')[:100]
        return object_list


# 1.9 可以有如下写法 api: https://docs.djangoproject.com/en/1.9/topics/class-based-views/intro/#decorating-the-class
@method_decorator(login_required, name='dispatch')
class CreateView(generic.CreateView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    success_url = '/blog/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if 'publish' in self.request.POST:
            post.publish()
        else:
            post.save()
            return redirect('blog:private')
        return super(CreateView, self).form_valid(form)


class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'


'''
user blog list
'''
def blogsList(request):
    return  render(request, 'blog/blogList.html', )


@login_required()
def new_blog(request):
    return  render(request, 'blog/edit.html', )
    # if request.method == "POST":
    #     form = QuestionForm(request.POST)
    #     if form.is_valid():
    #         form.clean()
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         if 'publish' in request.POST:
    #             post.publish()
    #             # return redirect('qs.views.index')
    #             return redirect(reverse_lazy('index'))
    #         else:
    #             post.save()
    #             return redirect('qs.views.draft_list')
    # else:
    #     form = QuestionForm()
    # return render(request, 'qs/edit.html', {'form': form})