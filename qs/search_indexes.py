#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from .models import Question
from haystack import indexes

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # env = indexes.CharField(document=True)
    # 对title字段进行索引
    title = indexes.CharField(model_attr='title')
    content_md = indexes.CharField(model_attr='env')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.all()