from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage

import os, time
from PIL import Image

from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from .forms import BaseRegisterForm, ChangepwdForm, RegisterForm, EmailForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

try:
    from repository.local_settings import EMAIL_HOST_USER
except:
    from repository.settings import EMAIL_HOST_USER

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
        context['next'] = next_str[next_str.find('next=')+5: -1]  # 处理next 值
        self.request.session['state'] = state
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LoginForm, self).form_valid(form)


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('forum:index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)