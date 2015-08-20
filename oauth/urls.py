from django.conf.urls import url

from .views import GithubOauthView, WeiboOauthView

urlpatterns = [
    url(r'^github$', GithubOauthView.as_view(), name='github_oauth'),
    url(r'^weibo$', WeiboOauthView.as_view(), name='weibo_oauth'),
    # url(r'^qq$', QQOauthView.as_view(), name='qq_oauth'),
]