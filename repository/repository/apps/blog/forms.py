# -*- coding: utf-8 -*-
from .models import Blog
from django import forms


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '标题：我是MAC黑！'}),
        }