from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlencode
import hashlib
import markdown
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)

    nickname = models.CharField(max_length=30)
    rank = models.IntegerField(default=0, editable=False, blank=True)
    voted = models.IntegerField(default=0, editable=False, blank=True)

    answers = models.IntegerField(default=0, editable=False, blank=True)
    questions = models.IntegerField(default=0, editable=False, blank=True)

    use_gravatar = models.BooleanField(default=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.URLField(default="http://www.gravatar.com/avatar/", blank=True, null=True)
    website = models.URLField(default='http://', blank=True, null=True)
    about_me = models.TextField()
    content_md = models.TextField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.content_md = markdown.markdown(
            self.about_me,
            safe_mode='escape',
            output_format='html5',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.sane_lists',
                'markdown.extensions.codehilite(noclasses=True, linenums=False)',
                'markdown.extensions.toc'
            ]
        )
        super(Profile, self).save(*args, **kwargs)

    def avatar(self):
        da = ''  # default avatar
        dic = {}
        if self.use_gravatar:
            mail = self.user.email.lower().encode('utf-8')
            gravatar_url = "http://www.gravatar.com/avatar/"
            base_url = gravatar_url + hashlib.md5(mail).hexdigest() + "?"
            dic['small'] = base_url + urlencode({'d': da, 's': '40'})
            dic['middle'] = base_url + urlencode({'d': da, 's': '48'})
            dic['large'] = base_url + urlencode({'d': da, 's': '80'})
            return dic
        elif self.avatar_url:
            dic['small'] = self.avatar_url
            dic['middle'] = self.avatar_url
            dic['large'] = self.avatar_url
        return dic

    def __str__(self):
        return self.user.username