# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlencode
import hashlib
import markdown


class Oauth(models.Model):
    '''

    '''
    user = models.ForeignKey(User)


