__author__ = 'mugbya'
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Profile

alphanumeric = RegexValidator(r'^[0-9a-zA-Z\_]{1,20}$')


class BaseRegisterForm(forms.Form):
    email = forms.EmailField(
        label=u'邮箱',
        help_text=u'邮箱可用于登录，最重要的是需要邮箱来找回密码，所以请输入您的可用邮箱。',
        max_length=50,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
    username = forms.CharField(
        label=u'昵称',
        help_text=u'昵称可用于登录，不能包含空格和@字符。',
        max_length=20,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            alphanumeric(username)
        except:
            raise forms.ValidationError(u'昵称中出现非法字符')
        res = User.objects.filter(username=username)
        if res:
            raise forms.ValidationError(u'此昵称已经注册，请重新输入')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        res = User.objects.filter(email=email)
        if res:
            raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
        return email


class RegisterForm(BaseRegisterForm):
    password = forms.CharField(
        label=u'密码',
        help_text=u'密码只有长度要求，长度为 6 ~ 18 。',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        profile = Profile()
        profile.user = user
        profile.save()

class ChangepwdForm(forms.Form):
    passpwd1 = forms.CharField(
        required=True,
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )

    passpwd2 = forms.CharField(
        required=True,
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['passpwd1'] != self.cleaned_data['passpwd2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data

