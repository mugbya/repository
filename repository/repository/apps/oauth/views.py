# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render, resolve_url, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import generic

from .models import Oauth
from django.contrib.auth.models import User
import requests
from .util import generator_token
from repository.config import local_settings

GITHUB_CLIENT_ID = local_settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = local_settings.GITHUB_CLIENT_SECRET
GITHUB_CALLBACK = local_settings.GITHUB_CALLBACK

#
# WEIBO_CLIENTID = local_settings.WEIBO_CLIENTID
# WEIBO_CLIENTSECRET = local_settings.WEIBO_CLIENTSECRET
# WEIBO_CALLBACK = local_settings.WEIBO_CALLBACK
#
# QQ_CLIENTID = local_settings.QQ_CLIENTID
# QQ_CLIENTSECRET = local_settings.QQ_CLIENTSECRET
# QQ_CALLBACK = local_settings.QQ_CALLBACK


def get_access_token(request, url, data):
    # try:
    #     state_session = request.session.pop('state')
    #     if state_session != data['state']:
    #         return None
    # except:
    #     return None
    response = requests.post(url, data=data, headers={'Accept': 'application/json'})
    result = response.json()
    return result


class GitHubView(generic.RedirectView):
    '''
    到第三方授权页，获取code
    '''

    url = 'https://github.com/login?client_id=' + GITHUB_CLIENT_ID \
          + '&return_to=/login/oauth/authorize?client_id=' + GITHUB_CLIENT_ID \
          + '&redirect_uri=' + GITHUB_CALLBACK  # &state=' + generator_token


class GitHubVerifyView(generic.RedirectView):

    def get_user_info(self, access_token):
        url = 'https://api.github.com/user'
        response = requests.get(url, params={'access_token': access_token})
        data = response.json()
        username = data['login']
        email = data['email']
        link_github = data['html_url']

        try:
            oauth = Oauth.objects.get(link_oauth=link_github)
            self.url = reverse('forum:index')
            user = User.objects.get(id=oauth.user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
        except:
            self.url = reverse('user:bind')

            self.request.session['typename'] = 'GitHub'
            self.request.session['type'] = TYPE_GitHub
            self.request.session['link'] = link_github
            self.request.session['email'] = email
            self.request.session['username'] = username

    def get_redirect_url(self, *args, **kwargs):
        '''
        获取github code 后,凭相关信息获取access_token
        :param args:
        :param kwargs:
        :return:
        '''
        code = self.request.GET.get('code')
        state = self.request.GET.get('state')
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code,
            'redirect_uri': GITHUB_CALLBACK,
            'state': state
        }
        try:
            access_token_info = get_access_token(self.request, url, data)
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except:
            messages.error(self.request, u'获取授权失败')
            return reverse('user:login')
        return super(GitHubVerifyView, self).get_redirect_url(*args, **kwargs)
