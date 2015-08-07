from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage

import os
from PIL import Image

from .models import Profile
from qs.models import Question, Solution
from .forms import ChangepwdForm, RegisterForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy

# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, 'media/upload')

storage = FileSystemStorage(
    location=UPLOAD_PATH,
    base_url='/media/upload/'
)



def userIndex(request, username):
    user = get_object_or_404(User, username=username)

    profile = get_object_or_404(Profile, user=user)
    questions = Question.objects.filter(author=user.id)
    solutions = Solution.objects.filter(author=user.id)
    return render(request, 'user/index.html', {'profile': profile,
                                               'email': user.email,
                                               'questions': questions,
                                               'solutions': solutions})

def settings(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        website = request.POST['website']
        about_me = request.POST['about_me']

        # try:
        #     alphanumeric(request.POST['username'])
        # except:
        #     return render(request, 'user/settings.html', {'error_messages': '用户名请不多于20个字符。只能用字母、数字和下划线'})

        if username != user.username and User.objects.filter(username=username).exists():
            return render(request, 'user/settings.html', {'error_messages': '用户名已经存在'})

        user.username = username
        user.email = email
        profile.about_me = about_me

        profile.website = website
        user.save()
        profile.save()
        # return render(request, 'user/index.html', {'profile': profile, 'email': user.email})
        # return redirect(reverse('user.views.index'), pk=user.username)
        # return redirect('userIndex', pk=user.username)
        return redirect('user.views.userIndex', username=user.username)
    return render(request, 'user/settings.html', {'profile': profile, 'email': user.email})

def resetpwd(request):
    user = request.user
    if request.POST:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            passpwd1 = request.POST['passpwd1']
            user.set_password(passpwd1)
            user.save()
            user = authenticate(username=user.username, password=passpwd1)
            login(request, user)
    return redirect('user.views.settings')

def uploadavatar_upload(request):
    u = request.user
    if request.method == 'POST':
        # f = request.FILES.get('uploadavatarfile', None)
        f = request.FILES['file']
        if f:
            extension = os.path.splitext(f.name)[-1]
            if (extension not in ['.jpg', '.png', '.gif']) or ('image' not in f.content_type):
                # return error(request, _('file type not permitted'))
                print("文件类型不对")
            im = Image.open(f)
            im.thumbnail((120,120))
            name = storage.get_available_name(str(u.id)) + '.png'
            url = storage.url(name)
            request.user.profile.avatar_url = url
            im.save('%s/%s' % (storage.location, name), 'PNG')
        u.profile.use_gravatar = False
        u.profile.save()
    return redirect('qs.views.index', )

class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)