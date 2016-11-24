# -*- coding: utf-8 -*-
from .models import Question
from django import forms


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '标题：你是MAC黑么'}),
        }