__author__ = 'mugbya'
from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'detailed')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '标题：我想和你一起'}),
        }