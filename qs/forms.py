# -*- coding: utf-8 -*-
__author__ = 'mugbya'

from django.contrib import admin

from django import forms
from .models import Question, Solution

class SolutionInline(admin.StackedInline):
    extra = 1
    model = Solution


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('category', 'tags', 'env',  'title', 'detailed')

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('content',)

# class SolutionForm(forms.ModelForm):
#     class Meta:
#         model = Solution
#         fields = ('content')