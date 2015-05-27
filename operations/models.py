# -*- coding: utf-8 -*-
from django.db import models

#    python  manage.py syncdb
#
# Create your models here.
#   Your models have changes that are not yet reflected in a migration, and so won't be applied.
#   Run 'python manage.py makemigrations' to make new migrations,
#       and then re-run ' python manage.py migrate' to apply them.
#

class Contact(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Tag(models.Model):
    contact = models.ForeignKey(Contact)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Classification(models.Model):
    # '''
    #    运维下的分类表
    # '''
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    # def __unicode__(self):
    #     return self.name

