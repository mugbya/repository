# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage


import os, time, re
from PIL import Image

from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from .forms import BaseRegisterForm, ChangepwdForm, RegisterForm, EmailForm
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
# try:
#     from repository.local_settings import EMAIL_HOST_USER
# except:
#     from repository.settings import EMAIL_HOST_USER

from .util import generator_token
import traceback


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, 'media/upload')

storage = FileSystemStorage(
    location=UPLOAD_PATH,
    base_url='/media/upload/'
)

import logging

logger = logging.getLogger(__name__)


class LoginForm(generic.FormView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('forum:index')
    form_class = AuthenticationForm

    def get_success_url(self):
        '''
        如果有next 值,怎跳转到next指向的值
        :return:
        '''
        next_url = self.request.POST.get('next', None)
        if next_url:
            return "%s" % (next_url)
        else:
            return reverse('forum:index')

    def get_context_data(self, **kwargs):
        '''
        处理oauth 的 state
        '''
        context = super(LoginForm, self).get_context_data(**kwargs)
        state = generator_token()
        context['state'] = state
        next_str = self.request.environ['QUERY_STRING']
        context['next'] = next_str[next_str.find('next=') + 5: -1]  # 处理next 值
        self.request.session['state'] = state
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LoginForm, self).form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LoginForm, self).form_valid(form)


class RegisterView(generic.TemplateView):
    template_name = "user/register.html"

    success_url = reverse_lazy('forum:index')

    def post(self, request):
        '''
        不用 form_valid --> 便于控制错误样式
        不用 ajax/JsonResponse --> 不用js来控制样式
        :param request:
        :return:
        '''
        try:
            username = request.POST.get('username', None)
            email = request.POST.get('email', None)
            password = request.POST.get('password', None)

            result = re.match('^[a-zA-Z][a-zA-Z0-9_]{1,20}$', username)

            if not username or len(username) > 20 or not result:
                messages.error(request, u'请输入不含特殊字符的用户名,且长度不要超过20')
                return render(request, 'user/register.html')

            if not password:
                messages.error(request, u'请输入密码')
                return render(request, 'user/register.html')

            user = User.objects.filter(username=username)
            if user:
                messages.error(request, u'该账户已经被注册')
                return render(request, 'user/register.html')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('forum:index')
        except Exception as e:
            messages.error(request, u'注册失败,请重试或者联系管理员')
            logger.error(u' 注册失败 ' + str(e))
            return render(request, 'user/register.html')


class ResetPWD(generic.View):
    '''
    充值密码
    '''
    def post(self, request):
        try:
            user = request.POST.get('user', None)
            password = request.POST.get('password', None)
            password_ = request.POST.get('password_', None)

            user = User.objects.filter(Q(username=user) | Q(email=user))
            if not user:
                messages.error(request, u'用户未注册')
                return redirect('user:login')
            user = user.first()

            if not password or not password_:
                messages.error(request, u'请输入密码')
                return redirect('user:login')
            if password != password_:
                messages.error(request, u'两次输入的密码不一致')
                return redirect('user:login')

            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            login(request, user)

            return redirect('forum:index')
        except Exception as e:
            messages.error(request, u'充值密码失败,请重试或者联系管理员')
            logger.error(u' 充值密码失败 ' + str(e))
            return redirect('user:login')


# class BindView(generic.FormView):
#     '''
#     绑定第三方
#     '''
#     template_name = 'user/bind.html'
#     success_url = reverse_lazy('index')
#     form_class = EmailForm
#
#     def form_valid(self, form):
#         email = form.cleaned_data['mail']
#         type = form.cleaned_data['type']
#         username = self.request.session['username']
#         link = self.request.session['link']
#         token = generator_token()
#         self.request.session['token'] = token
#         self.request.session['time'] = time.time()
#         self.request.session['email'] = email
#
#         opts = {
#             'token': token,
#             'from_email': EMAIL_HOST_USER,
#             'username': username,
#             'typename': oauth_type[type],
#             'link': link,
#             'html_email_template_name': 'user/email/bind_oauth.html',
#         }
#         form.save(**opts)
#
#         messages.success(self.request, "一封确认邮件已经发送至" + email + "，请根据提示完成绑定")
#         return super(BindView, self).form_valid(form)