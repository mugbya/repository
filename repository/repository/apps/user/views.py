# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.core.files.storage import FileSystemStorage

from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode

from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _

import os, time, re, requests
from PIL import Image

from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from .forms import BaseRegisterForm, ChangepwdForm, RegisterForm, EmailForm
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

from repository.config import settings

try:
    from repository.config.local_settings import EMAIL_API_KEY, EMAIL_API_USER, DOMAIN
except:
    from repository.config.settings import EMAIL_API_KEY, EMAIL_API_USER, DOMAIN

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
    success_url = reverse_lazy('base:index')
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
            return reverse('base:index')

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

    success_url = reverse_lazy('base:index')

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

            return redirect('base:index')
        except Exception as e:
            messages.error(request, u'注册失败,请重试或者联系管理员')
            logger.error(u' 注册失败 ' + str(e))
            return render(request, 'user/register.html')


def password_reset_confirm(request, uidb64=None, token=None):
    '''
    重置密码
    :param request:
    :param uidb64:
    :param token:
    :return:
    '''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if request.method == 'GET':
            return render(request, 'registration/password_reset_confirm.html')
        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST.get('password', None)
                password_ = request.POST.get('password_', None)

                if not password or not password_:
                    messages.error(request, u'请输入密码')
                    return redirect('/user/reset/' + uidb64 + '/' + token + '/')
                if password != password_:
                    messages.error(request, u'两次输入的密码不一致')
                    return redirect('/user/reset/' + uidb64 + '/' + token + '/')

                user.set_password(password)
                user.save()
                user = authenticate(username=user.username, password=password)
                login(request, user)

                return redirect('base:index')

        else:
            messages.error(request, u'密码已经重置，该链接无效')
            return redirect('/user/reset/' + uidb64 + '/' + token + '/')
    except Exception as e:
        messages.error(request, u'重置密码失败,请重试或者联系管理员')
        logger.error(u' 重置密码失败 ' + str(e))
        return redirect('user:login')


def password_reset_complete(request, template_name='registration/password_reset_complete.html', extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@csrf_protect
def password_reset(request):
    '''
    重置密码，发送邮件
    :param request:
    :return:
    '''
    if request.method == "POST":
        to_email = request.POST.get('email', None)
        if not to_email:
            messages.error(request, u'邮件填写错误')
            return redirect("password_reset")

        use_https = False
        url = "http://sendcloud.sohu.com/webapi/mail.send.json"
        for user in User.objects.filter(email=to_email):
            if DOMAIN:  # TODO not
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = DOMAIN

            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            body = loader.render_to_string('registration/password_reset_email.html', context)

            params = {"api_user": EMAIL_API_USER,
                      "api_key": EMAIL_API_KEY,
                      "from": EMAIL_API_USER + "@" + DOMAIN,
                      "fromname": "Repository社区",
                      "to": to_email,
                      "subject": "密码重置",
                      "html": body,
                      "resp_email_id": "true"
                      }
            res = requests.post(url, files={}, data=params)
        return redirect("password_reset_done")
    elif request.method == "GET":
        return render(request, 'registration/password_reset_form.html')


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
