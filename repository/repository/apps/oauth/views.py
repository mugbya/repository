# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render

from django.views import generic

from repository.config import local_settings

GITHUB_CLIENT_ID = local_settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = local_settings.GITHUB_CLIENT_SECRET


# GITHUB_CALLBACK = local_settings.GITHUB_CALLBACK
#
# WEIBO_CLIENTID = local_settings.WEIBO_CLIENTID
# WEIBO_CLIENTSECRET = local_settings.WEIBO_CLIENTSECRET
# WEIBO_CALLBACK = local_settings.WEIBO_CALLBACK
#
# QQ_CLIENTID = local_settings.QQ_CLIENTID
# QQ_CLIENTSECRET = local_settings.QQ_CLIENTSECRET
# QQ_CALLBACK = local_settings.QQ_CALLBACK

class GithubView(generic.RedirectView):
    '''
    %2F  /
    %3F  ?
    %3D  =
    %26

    <a href="https://githubGithubView.com/login/oauth/authorize?
    client_id=dd90d6225d6bb60bf7a5&redirect_uri=http://127.0.0.1:8000/oauth/github&state={{ state }}"#}

    https://github.com/login?client_id=dd90d6225d6bb60bf7a5&
    return_to=/login/oauth/authorize?
    client_id=f6b8a50f7dfce7e05adb&
    redirect_uri=https%3A%2F%2Fsegmentfault.com%2Fuser%2Foauth%2Fgithub

    https://github.com/login/oauth/access_token
   '''

    url = 'https://github.com/login?client_id=' + GITHUB_CLIENT_ID \
          + '&return_to=/login/oauth/authorize?client_id=' + GITHUB_CLIENT_ID \
          + '&redirect_uri=https://segmentfault.com/user/oauth/github'
