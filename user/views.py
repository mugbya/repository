from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 ,render,redirect
from django.core.files.storage import FileSystemStorage

from django.core.validators import RegexValidator
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


from .models import Profile


# Create your views here.

# storage = FileSystemStorage(
#     location=conf.UPLOAD_PATH,
#     base_url='/static/upload/'
# )

alphanumeric = RegexValidator(r'^[0-9a-zA-Z\_]{1,20}$', 'Only alphanumeric characters and underscore are allowed.')

def index(request, username):
    user = get_object_or_404(User, username__contains=username)

    profile = get_object_or_404(Profile, user=user)
    return render(request, 'user/index.html', {'profile': profile, 'email': user.email})

def settings(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        website = request.POST['website']
        about_me = request.POST['about_me']

        try:
            alphanumeric(request.POST['username'])
        except:
            return render(request, 'user/settings.html', {'error_messages': '用户名请不多于20个字符。只能用字母、数字和下划线'})

        if User.objects.filter(username=username).exists():
            return render(request, 'user/settings.html', {'error_messages': '用户名已经存在'})

        user.username = username
        user.email = email
        profile.about_me = about_me

        profile.website = website
        user.save()
        profile.save()
        return render(request, 'user/index.html', {'profile': profile, 'email': user.email})
    return render(request, 'user/settings.html', {'profile': profile, 'email': user.email})

def avatar(request):
    pass

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        try:
            alphanumeric(request.POST['username'])
        except:
            return render(request, 'registration/register.html', {'error_messages': '用户名请不多于20个字符。只能用字母、数字和下划线'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error_messages': '用户名已经存在'})

        user = User.objects.create_user(username, None, password)
        user = authenticate(username=username, password=password)
        login(request, user)
        profile = Profile()
        profile.user = user
        profile.save()

        return redirect('qs.views.index', )

    return render(request, "registration/register.html")

