
import requests
from user.models import Profile
from oauth.models import Oauth
# from requests.conf import settings
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect

from django.core.urlresolvers import reverse_lazy, reverse

import traceback

# GITHUB_CLIENTID = settings.GITHUB_CLIENTID
# GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
# GITHUB_CALLBACK = settings.GITHUB_CALLBACK


TYPE_GitHub = 1
oauth_type = {1: 'Github', 2: 'Weibo'}

GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_CLIENTID = 'dd90d6225d6bb60bf7a5'
GITHUB_CLIENTSECRET = '1e8ae44e78831f1831e7be2755201d30b3ea2e0c'
GITHUB_CALLBACK = 'http://127.0.0.1:8000/oauth/github'


def hander():
    pass

class GithubOauthView(RedirectView):
    permanent = False

    def get_access_token(self):
        code = self.request.GET.get('code')
        state = self.request.GET.get('state')
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': GITHUB_CLIENTID,
            'client_secret': GITHUB_CLIENTSECRET,
            'code': code,
            'redirect_uri': GITHUB_CALLBACK,
            'state': state
        }
        try:
            response = requests.post(url, data=data, headers={'Accept': 'application/json'})
            result = response.json()
        except :
            traceback.print_exc()
            # raise "请求失败"
        return result

    def get_user_info(self, access_token):
        url = 'https://api.github.com/user'
        response = requests.get(url, params={'access_token': access_token})
        data = response.json()
        print(data)
        username = data['login']
        email = data['email']
        link_github = data['html_url']

        try:
            oauth = Oauth.objects.get(link_oauth = link_github )
            self.url = reverse('index')
            user = User.objects.get(id=oauth.user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            # user = User.objects.get(email=email)
            # print(user)
            # users = User.objects.get(username=username)
            # print(users)
            # profile = Profile.objects.get(user=user)
            # print(profile.use_github)
            # if profile.use_github:
            #     self.url = 'http://127.0.0.1:8000'
            # else:
            #     redirect('bind', {'type': 'github'})
        except:
            self.url = reverse('bind')

            self.request.session['typename'] = 'GitHub'
            self.request.session['type'] = TYPE_GitHub
            self.request.session['link'] = link_github
            self.request.session['email'] = email
            self.request.session['username'] = username

    def get_redirect_url(self, *args, **kwargs):
        try:
            access_token_info = self.get_access_token()
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except :
            traceback.print_exc()
        return super(GithubOauthView, self).get_redirect_url(*args, **kwargs)