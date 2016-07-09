# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
import uuid
import markdown
from django.db.models.query import QuerySet


# python3 manage.py makemigrations blog
# python3 manage.py migrate


class PostBase(models.Model):
    '''
    基类
    '''
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    voted = models.IntegerField(default=0, editable=False, blank=True)
    content_md = models.TextField(editable=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        abstract = True


class Blog(PostBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, error_messages={
        'blank': "标题不能为空",
        'null': "标题不能为空",
        'invalid': "您输入了一个无效的标题，标题的长度请控制在100个字符内"
    }, verbose_name=u"标题")
    detailed = models.TextField(error_messages={}, verbose_name=u"正文")
    count_click = models.IntegerField(default=0)  # 浏览量

    def save(self, *args, **kwargs):
        self.content_md = markdown.markdown(
            self.detailed,
            safe_mode='escape',
            output_format='html5',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.sane_lists',
                'markdown.extensions.codehilite(noclasses=True, linenums=False)',
                'markdown.extensions.toc'
            ]
        )
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})  # args=[str(self.id)]

    def __str__(self):
        return self.title


class Comment(PostBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    content = models.TextField(error_messages={}, )

    def get_absolute_url(self):
        if getattr(self.blog, 'pk', None):
            return reverse('blog:detail', kwargs={'pk': self.blog.pk})

        return reverse('blog:index')

    def __str__(self):
        return self.content


#相关文档: https://segmentfault.com/a/1190000005875158
class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model, using=self._db)

    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)


class Recommend(models.Model):
    '''
    推荐功能
    '''
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # 推荐状态

    objects = QuerySetManager()

    class QuerySet(QuerySet):

        def get_or_none(self, *args, **kwargs):
            """
            Performs the query and returns a single object matching the given
            keyword arguments.
            """
            clone = self.filter(*args, **kwargs)
            if self.query.can_filter() and not self.query.distinct_fields:
                clone = clone.order_by()
            num = len(clone)
            if num == 1:
                return clone._result_cache[0]
            if not num:
                return None


class Favorite(models.Model):
    '''
    收藏夹功能
    '''
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # 收藏状态

    objects = QuerySetManager()

    class QuerySet(QuerySet):

        def get_or_none(self, *args, **kwargs):
            """
            Performs the query and returns a single object matching the given
            keyword arguments.
            """
            clone = self.filter(*args, **kwargs)
            if self.query.can_filter() and not self.query.distinct_fields:
                clone = clone.order_by()
            num = len(clone)
            if num == 1:
                return clone._result_cache[0]
            if not num:
                return None