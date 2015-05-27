# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'名称')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'名称')
    count_post = models.IntegerField(default=0, editable=False, verbose_name=u'条数')
    category = models.ManyToManyField(Category, blank=True, verbose_name=u'分类')

    def __str__(self):
        return self.name


class Qs(models.Model):
    env = models.CharField(max_length=200)
    brief = models.CharField(max_length=200)
    detailed = models.TextField(max_length=99999)
    solution = models.TextField(max_length=99999,blank=True)
    q_data = models.DateField(auto_now_add=True)
    s_date = models.DateField(auto_now_add=True)
    Author = models.CharField(max_length=50)
    Solvers = models.CharField(max_length=50,blank=True)
    is_solver = models.BooleanField(editable=False, blank=True, default=False)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')
    category = models.OneToOneField(Category, blank=True, verbose_name=u'分类')

    def __str__(self):
        return self.brief



