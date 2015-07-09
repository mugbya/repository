from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 ,render,redirect

from .models import Profile
# Create your views here.

def index(request, username):

    user = get_object_or_404(User, username__contains=username)

    # profile = get_object_or_404(Profile, nickname__=username)
    return render(request, 'user/index.html', {'profile': user})
    # return redirect('qs.views.index')

def settings(request):
    pass

def avatar(request):
    pass

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user.username)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, user)
            return redirect('qs.views.index', )
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})

