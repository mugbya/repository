from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from django.utils.decorators import method_decorator

from .models import Blog, Recommend, Favorite
from .forms import BlogForm
from repository.settings import PAGE_NUM

import logging
logger = logging.getLogger(__name__)


# class BaseMixin(object):
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(BaseMixin, self).get_context_data(**kwargs)
#         try:
#             pass
#         except Exception as e:
#             logger.error(u'[BaseMixin]加载基本信息出错')
#         return context


class IndexView(generic.ListView):
    '''
    all blog list
    '''
    paginate_by = PAGE_NUM
    template_name = 'blog/index.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['index_active'] = True
        context['newest_active'] = False
        return context

    def get_queryset(self):
        object_list = Blog.objects.filter(published_date__isnull=False, is_active=True).order_by('voted', '-published_date')[:100]
        return object_list


class NewestView(generic.ListView):
    '''
    all blog list
    '''
    paginate_by = PAGE_NUM
    template_name = 'blog/index.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(NewestView, self).get_context_data(**kwargs)
        context['index_active'] = False
        context['newest_active'] = True
        return context

    def get_queryset(self):
        object_list = Blog.objects.filter(published_date__isnull=False, is_active=True).order_by('-published_date')
        return object_list


class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        recommend_list = Recommend.objects.filter(blog=self.object, status=True)

        voted_status = '推荐'
        if not self.request.user.is_anonymous():
            recommend = Recommend.objects.get_or_none(blog=self.object, user=self.request.user)
            if recommend and recommend.status:
                voted_status = '已推荐'

        context['voted_status'] = voted_status
        context['voted'] = len(recommend_list)
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


# @method_decorator(login_required, name='dispatch')
class VotedView(generic.View):

    def post(self, request, *args, **kwargs):
        '''
        有关ajax 相关的处理请参看 www.ziqiangxuetang.com 跟下面具体的链接
        http: // www.ziqiangxuetang.com / django / django - ajax.html
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        status = '推荐'
        id = request.POST['id'][request.POST['id'].find('/blog/', ) + 6:-1]
        if request.user.is_anonymous():
            return redirect('/user/login/?next=%s' % '/blog/'+id+'/')

        if request.is_ajax():
            blog = get_object_or_404(Blog, pk=id)
            if not request.user.is_anonymous():
                recommend = Recommend.objects.get_or_none(blog=blog, user=request.user)
            if '推荐' == request.POST['content']:
                status = '已推荐'
                # 用户可能测试频繁操作推荐功能,故此不能重复创建与删除,而是应该创建一次,其后操作更改状态即可
                if recommend:
                    recommend.status = True
                else:
                    recommend = Recommend(blog=blog, user=request.user, status=True)
            else:
                if recommend:
                    recommend.status = False
            recommend.save()

            recommend_list = Recommend.objects.filter(blog=blog, status=True)

            return JsonResponse({'status': status, 'voted': len(recommend_list)})


