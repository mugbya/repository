from django.conf.urls import url

from .views import GithubOauthView

urlpatterns = [
    url(r'^github$', GithubOauthView.as_view(), name='github_oauth'),
]