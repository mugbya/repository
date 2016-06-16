from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage

import os, time
from PIL import Image

from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from oauth.views import  oauth_type
from oauth.models import Oauth
from qs.models import Question, Solution
from .forms import BaseRegisterForm, ChangepwdForm, RegisterForm, EmailForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

from repository.local_settings import EMAIL_HOST_USER

from .util import generator_token
import traceback
from django.contrib import messages
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, 'media/upload')

storage = FileSystemStorage(
    location=UPLOAD_PATH,
    base_url='/media/upload/'
)


class LoginForm(FormView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('index')
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        '''
        处理oauth 的 state
        '''
        context = super(LoginForm, self).get_context_data(**kwargs)
        state = generator_token()
        context['state'] = state
        self.request.session['state'] = state
        return context


    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LoginForm, self).form_valid(form)


def userIndex(request, username):
    user = get_object_or_404(User, username=username)

    profile = get_object_or_404(Profile, user=user)
    oauth_list = Oauth.objects.filter(user_id=user.id)
    questions = Question.objects.filter(author=user.id)
    solutions = Solution.objects.filter(author=user.id)
    return render(request, 'user/index.html', {'profile': profile,
                                               'email': user.email,
                                               'questions': questions,
                                               'solutions': solutions,
                                               'oauth_list': oauth_list})

def settings(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    oauth_list = Oauth.objects.filter(user_id=user.id)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        website = request.POST['website']
        about_me = request.POST['about_me']

        # try:
        #     alphanumeric(request.POST['username'])
        # except:
        #     return render(request, 'user/settings.html', {'error_messages': '用户名请不多于20个字符。只能用字母、数字和下划线'})

        if username != user.username and User.objects.filter(username=username).exists():
            return render(request, 'user/settings.html', {'error_messages': '用户名已经存在'})

        user.username = username
        user.email = email
        profile.about_me = about_me

        profile.website = website
        user.save()
        profile.save()
        # return render(request, 'user/index.html', {'profile': profile, 'email': user.email})
        # return redirect(reverse('user.views.index'), pk=user.username)
        # return redirect('userIndex', pk=user.username)
        return redirect('user.views.userIndex', username=user.username)
    return render(request, 'user/settings.html', {'profile': profile,
                                                  'email': user.email,
                                                  'oauth_list': oauth_list})

def resetpwd(request):
    user = request.user
    if request.POST:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            passpwd1 = request.POST['passpwd1']
            user.set_password(passpwd1)
            user.save()
            user = authenticate(username=user.username, password=passpwd1)
            login(request, user)
    return redirect('user.views.settings')

def uploadavatar_upload(request):
    u = request.user
    if request.method == 'POST':
        # f = request.FILES.get('uploadavatarfile', None)
        f = request.FILES['file']
        if f:
            extension = os.path.splitext(f.name)[-1]
            if (extension not in ['.jpg', '.png', '.gif']) or ('image' not in f.content_type):
                # return error(request, _('file type not permitted'))
                print("文件类型不对")
            im = Image.open(f)
            im.thumbnail((120,120))
            name = storage.get_available_name(str(u.id)) + '.png'
            url = storage.url(name)
            request.user.profile.avatar_url = url
            im.save('%s/%s' % (storage.location, name), 'PNG')
        u.profile.is_use_gravatar = False
        u.profile.save()
    return redirect('qs.views.index', )

class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)


class BindView(FormView):
    '''
    绑定已有账户（发送邮件信息）
    '''
    template_name = 'user/bind.html'
    success_url = reverse_lazy('index')
    form_class = EmailForm

    def form_valid(self, form):
        email = form.cleaned_data['mail']
        type = form.cleaned_data['type']
        username = self.request.session['username']
        link = self.request.session['link']
        token = generator_token()
        self.request.session['token'] = token
        self.request.session['time'] = time.time()
        self.request.session['email'] = email

        opts = {
            'token': token,
            'from_email': EMAIL_HOST_USER,
            'username': username,
            'typename': oauth_type[type],
            'link': link,
            'html_email_template_name': 'user/email/bind_oauth.html',
        }
        form.save(**opts)

        messages.success(self.request, "一封确认邮件已经发送至" + email + "，请根据提示完成绑定")
        return super(BindView, self).form_valid(form)


class BindNewUserView(FormView):
    '''
    绑定成为新用户
    '''
    template_name = 'user/bind.html'
    form_class = BaseRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        link = self.request.session.pop('link')
        type = self.request.session.pop('type')

        user = User.objects.create_user(username, email)
        user.save()

        profile = Profile(user=user)
        profile.save()

        oauth = Oauth(type_oauth=type, link_oauth=link, user=user)
        oauth.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super(BindNewUserView, self).form_valid(form)


def bindConfirm(request, token):
    '''
    绑定第三方信息，
    :param request:
    :param token:
    :return:
    '''
    try:
        time1 = request.session.pop('time')
        token_session = request.session.pop('token')
        email = request.session.pop('email')
        type = request.session.pop('type')
        link = request.session.pop('link')
        interval = time.time() - time1
        if interval > 3600 or token != token_session:
             messages.error(request, "链接错误或者已经失效")
             return redirect('index', )
    except:
        messages.error(request, "链接错误或者已经失效")
        return redirect('index', )

    user = User.objects.filter(email=email)[0]

    oauth = Oauth(type_oauth=type, link_oauth=link, user=user)
    oauth.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return redirect('user.views.userIndex', username=user.username)




