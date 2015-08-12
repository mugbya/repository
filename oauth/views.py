import urllib
# import urllib2
import requests
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login


GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK

class GithubOauthView(RedirectView):
    permanent = False
    url = None

    def get_access_token(self):
        code = self.request.GET.get('code')
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': GITHUB_CLIENTID,
            'client_secret': GITHUB_CLIENTSECRET,
            'code': code,
            'redirect_uri': GITHUB_CALLBACK,
        }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers={'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        result = response.read()
        result = json.loads(result)
        return result

    def get_user_info(self, access_token):
        url = 'https://api.github.com/user?access_token=%s' % (access_token)
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html)
        username = data['login'] + '(github_oauth)'
        email = 'oauth@oauth.com'
        password = '********'
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, email, password)
            user.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.GET.get('state')
        try:
            access_token_info = self.get_access_token()
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except:
            pass
        return super(GithubOauthView, self).get_redirect_url(*args, **kwargs)