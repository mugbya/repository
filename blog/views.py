from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import Blog


class IndexView(generic.ListView):
    '''
    all blog list
    '''
    template_name = 'blog/index.html'
    # context_object_name = 'blog_list'

    def get_queryset(self):
        return Blog.objects.order_by('-published_date')[:10]


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