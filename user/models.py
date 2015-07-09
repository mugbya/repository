from django.db import models
from django.contrib.auth.models import User
import urllib
import hashlib
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)

    rank = models.IntegerField(default=0, editable=False, blank=True)
    voted = models.IntegerField(default=0, editable=False, blank=True)

    answers = models.IntegerField(default=0, editable=False, blank=True)
    questions = models.IntegerField(default=0, editable=False, blank=True)

    use_gravatar = models.BooleanField(default=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    website = models.URLField(default='http://', blank=True, null=True)

    def avatar(self):
        da = ''  # default avatar
        dic = {}
        if self.use_gravatar:
            mail = self.user.email.lower()
            gravatar_url = "http://www.gravatar.com/avatar/"
            base_url = gravatar_url + hashlib.md5(mail).hexdigest() + "?"
            dic['small'] = base_url + urllib.urlencode({'d': da, 's': '40'})
            dic['middle'] = base_url + urllib.urlencode({'d': da, 's': '48'})
            dic['large'] = base_url + urllib.urlencode({'d': da, 's': '80'})
            return dic
        elif self.avatar_url:
            dic['small'] = self.avatar_url
            dic['middle'] = self.avatar_url
            dic['large'] = self.avatar_url
        return dic

    def __str__(self):
        return self.user.username