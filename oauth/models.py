from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Oauth(models.Model):
    # use_github = models.BooleanField(default=False)
    # use_google = models.BooleanField(default=False)
    # use_weibo = models.BooleanField(default=False)
    # use_qq = models.BooleanField(default=False)
    #
    # link_github = models.URLField(blank=True, null=True)
    # link_google = models.URLField(blank=True, null=True)
    # link_weibo = models.URLField(blank=True, null=True)
    # link_qq = models.URLField(blank=True, null=True)

    link_oauth = models.URLField(blank=True, null=True)
    type_oauth = models.IntegerField(editable=False, blank=True)

    user = models.ForeignKey(User)

    def __str__(self):
        return self.link_oauth

