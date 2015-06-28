# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
import markdown


#    python  manage.py syncdb
#
# Create your models here.
#   Your models have changes that are not yet reflected in a migration, and so won't be applied.
#   Run 'python manage.py makemigrations' to make new migrations,
#       and then re-run ' python manage.py migrate' to apply them.
#


class PostBase(models.Model):
    author = models.ForeignKey(User, null=True,  on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    content_md = models.TextField(editable=False, blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        abstract = True



class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'名称')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'描述')
    count_post = models.IntegerField(default=0, editable=False, verbose_name=u'条数')

    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'slug': self.pk})

    def __str__(self):
        return self.name

class Question(PostBase):
    env = models.CharField(max_length=200, verbose_name=u"环境")
    title = models.CharField(max_length=100, error_messages={
        'blank': "标题不能为空",
        'null': "标题不能为空",
        'invalid': "您输入了一个无效的标题，标题的长度请控制在100个字符内"
    }, verbose_name=u"标题")
    detailed = models.TextField(error_messages={},
                                verbose_name=u"详细内容")
    is_solver = models.BooleanField(editable=False, blank=True, default=False)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')

    count_vote = models.IntegerField(default=0, editable=False, blank=True)

    count_solution = models.IntegerField(default=0, editable=False, blank=True)

    count_link = models.IntegerField(default=0, editable=False, blank=True)

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
        super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

    def get_full_url(self):
        return getattr(settings, "ABSOLUTE_URL_PREFIX", "http://localhost") + self.get_absolute_url()

    def get_author_info(self):
            if self.author:
                return self.author.username, self.author.email

    def __str__(self):
        return self.title



class Solution(PostBase):
    question = models.ForeignKey(Question)

    content = models.TextField(error_messages={},)

    def save(self, *args, **kwargs):
        self.content_md = markdown.markdown(
            self.content,
            safe_mode='escape',
            output_format='html5',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.sane_lists',
                'markdown.extensions.codehilite(noclasses=True, linenums=False)',
                'markdown.extensions.toc'
            ]
        )
        super(Solution, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if getattr(self.question, 'pk', None):
            return reverse('question-detail', kwargs={'pk': self.question.pk})

        return reverse('index')

    def __str__(self):
        return self.content
