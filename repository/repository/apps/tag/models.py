# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=200)
    content_md = models.TextField(null=True, blank=True)

