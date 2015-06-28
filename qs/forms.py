# -*- coding: utf-8 -*-
__author__ = 'mugbya'

# from django.contrib import admin

from django import forms
from .models import Question, Solution

# class SolutionInline(admin.StackedInline):
#     extra = 1
#     model = Solution


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('env',  'title', 'detailed')
        widgets = {
            'env': forms.TextInput(attrs={'placeholder': '环境：简述环境'}),
            'title': forms.TextInput(attrs={'placeholder': '标题：一句话说清你遇到的开发问题'}),
        }

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('content',)

