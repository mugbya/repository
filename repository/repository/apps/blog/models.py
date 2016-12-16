# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
import uuid
import markdown

from tag.models import Tag


class BasePost(models.Model):
    '''
    问答基类
    '''
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    content_md = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Blog(BasePost):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    title = models.CharField(max_length=100, error_messages={'blank': "标题不能为空", 'null': "标题不能为空",
                                                             'invalid': "您输入了一个无效的标题，标题的长度请控制在100个字符内"})
    content = models.TextField(null=True)

    tags = models.ManyToManyField(Tag, null=True)

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

        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


