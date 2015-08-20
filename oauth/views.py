import requests
from oauth.models import Oauth
from repository import local_settings
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.contrib import messages

import traceback
import json

GITHUB_CLIENTID = local_settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = local_settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = local_settings.GITHUB_CALLBACK

WEIBO_CLIENTID = local_settings.WEIBO_CLIENTID
WEIBO_CLIENTSECRET = local_settings.WEIBO_CLIENTSECRET
WEIBO_CALLBACK = local_settings.WEIBO_CALLBACK

QQ_CLIENTID = local_settings.QQ_CLIENTID
QQ_CLIENTSECRET = local_settings.QQ_CLIENTSECRET
QQ_CALLBACK = local_settings.QQ_CALLBACK

TYPE_GitHub = 1
TYPE_Weibo = 2
TYPE_QQ = 3
oauth_type = {TYPE_GitHub: 'Github', TYPE_Weibo: '新浪微博', TYPE_QQ: '腾讯QQ'}


def get_access_token(request, url, data):
    try:
        state_session = request.session.pop('state')
        if state_session != data['state']:
            return None
    except:
        return None
    response = requests.post(url, data=data, headers={'Accept': 'application/json'})
    result = response.json()
    return result


class GithubOauthView(RedirectView):
    permanent = False

    def get_user_info(self, access_token):
        url = 'https://api.github.com/user'
        response = requests.get(url, params={'access_token': access_token})
        data = response.json()
        username = data['login']
        email = data['email']
        link_github = data['html_url']

        try:
            oauth = Oauth.objects.get(link_oauth=link_github)
            self.url = reverse('index')
            user = User.objects.get(id=oauth.user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
        except:
            self.url = reverse('bind')

            self.request.session['typename'] = 'GitHub'
            self.request.session['type'] = TYPE_GitHub
            self.request.session['link'] = link_github
            self.request.session['email'] = email
            self.request.session['username'] = username

    def get_redirect_url(self, *args, **kwargs):
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
            access_token_info = get_access_token(self.request, url, data)
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except:
            messages.error(self.request, '获取授权失败')
            return reverse('index')
        return super(GithubOauthView, self).get_redirect_url(*args, **kwargs)


class WeiboOauthView(RedirectView):
    permanent = False

    def get_user_info(self, access_token):
        url = 'https://api.weibo.com/oauth2/get_token_info'
        response = requests.post(url, data={'access_token': access_token})
        data = response.json()
        uid = data['uid']
        url = 'https://api.weibo.com/2/users/show.json'

        response = requests.get(url, params={'access_token': access_token, 'uid': uid})
        username = response.json().get('name', '')

        link_weibo = 'http://weibo.com/' + str(uid)

        try:
            oauth = Oauth.objects.get(link_oauth=link_weibo)
            self.url = reverse('index')
            user = User.objects.get(id=oauth.user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
        except:
            self.url = reverse('bind')

            self.request.session['typename'] = '新浪微博'
            self.request.session['type'] = TYPE_Weibo
            self.request.session['link'] = link_weibo
            self.request.session['email'] = ''
            self.request.session['username'] = username

    def get_redirect_url(self, *args, **kwargs):

        code = self.request.GET.get('code')
        state = self.request.GET.get('state')
        url = 'https://api.weibo.com/oauth2/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': WEIBO_CLIENTID,
            'client_secret': WEIBO_CLIENTSECRET,
            'code': code,
            'redirect_uri': WEIBO_CALLBACK,
            'state': state,
        }
        try:
            access_token_info = get_access_token(self.request, url, data)
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except :
            messages.error(self.request, '获取授权失败')
            return reverse('index')
        return super(WeiboOauthView, self).get_redirect_url(*args, **kwargs)


# class QQOauthView(RedirectView):
#     permanent = False
#
#     def get_access_token(self, url, data):
#         try:
#             state_session = self.request.session.pop('state')
#             if state_session != data['state']:
#                 return None
#         except:
#             return None
#         response = requests.get(url, params=data)
#         response = response.text
#         result = response[response.find('=')+1:response.find('&expires_in')]
#         return result
#
#     def get_user_info(self, access_token):
#         url = 'https://graph.qq.com/oauth2.0/me'
#         # response = requests.post(url, params={'access_token': access_token})
#         response = requests.get(url, params={'access_token': access_token})
#         data = response.text
#         data = data[data.find('{'):data.find('}')+1]
#         data = json.loads(data)
#
#         openid = data['openid']
#         # {'openid': '1E43D4D9DAB7F92454F574228AB2E0E4', 'client_id': '101240199'}
#
#         url = 'https://graph.qq.com/user/get_user_info'
#         payload = {'access_token': access_token,
#                    'oauth_consumer_key': QQ_CLIENTID,
#                    'openid': openid,
#                    'format': 'json'}
#         response = requests.get(url, params=payload)
#         username = response.json().get('nickname', '')
#
#         link_qq = str(openid)   # 提供奇葩的格式，这儿除了变数据结构外，就只有放弃接入它了
#
#         try:
#             oauth = Oauth.objects.get(link_oauth=link_qq)
#             self.url = reverse('index')
#             user = User.objects.get(id=oauth.user_id)
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             login(self.request, user)
#         except:
#             self.url = reverse('bind')
#
#             self.request.session['typename'] = '腾讯QQ'
#             self.request.session['type'] = TYPE_QQ
#             self.request.session['link'] = ''
#             self.request.session['email'] = ''
#             self.request.session['username'] = username
#
#     def get_redirect_url(self, *args, **kwargs):
#         code = self.request.GET.get('code')
#         state = self.request.GET.get('state')
#         url = 'https://graph.qq.com/oauth2.0/token'
#         data = {
#             'grant_type': 'authorization_code',
#             'client_id': QQ_CLIENTID,
#             'client_secret': QQ_CLIENTSECRET,
#             'code': code,
#             'redirect_uri': QQ_CALLBACK,
#             'state': state,
#         }
#         try:
#             access_token = self.get_access_token(url, data)
#             self.get_user_info(access_token)
#         except :
#             traceback.print_exc()
#             messages.error(self.request, '获取授权失败')
#             return reverse('index')
#         return super(QQOauthView, self).get_redirect_url(*args, **kwargs)