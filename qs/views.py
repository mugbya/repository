# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404 ,render,redirect
from django.views.generic import ListView, CreateView, FormView, TemplateView

from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput
from django.utils.six import BytesIO
from django.contrib.auth.decorators import login_required


from .forms import QuestionForm, SolutionForm

from haystack.forms import SearchForm

from .models import *



def index(request):
    # question_list = Question.objects.all()
    question_list = Question.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'qs/index.html', {'post_latest': question_list[:10]})


def detail(request, pk):
    detail_qs = get_object_or_404(Question, pk=pk)
    solution = detail_qs.solution_set
    solution_list = solution.all()
    solution_count = solution.count()
    if request.method == "POST":
        form = SolutionForm(request.POST, instance=Solution())
        if form.is_valid():
            solution = form.save(commit=False)
            solution.question = detail_qs
            solution.author = request.user
            solution.save()

            detail_qs.count_solution += 1
            detail_qs.save()
            return redirect('qs.views.detail', pk=pk)
    else:
        form = SolutionForm(instance=Solution())

    detail_qs.count_link += 1
    detail_qs.save()
    return render(request, 'qs/node/detail.html', {'detail_qs': detail_qs,
                                                   'solutions': solution_list,
                                                   'count': solution_count,
                                                   'form': form})
@login_required
def del_qs(request,pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('qs.views.index')

@login_required()
def new_qs(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:
                post.publish()
                return redirect('qs.views.index')
            else:
                post.save()
                return redirect('qs.views.draft_list')
    else:
        form = QuestionForm()
    return render(request, 'qs/edit.html', {'form': form})

@login_required
def edit_qs(request, pk):
    post = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = None
            if 'publish' in request.POST:
                post.publish()
                return redirect('qs.views.index')
            else:
                post.save()
                return redirect('qs.views.draft_list')
    else:
        form = QuestionForm(instance=post)
    return render(request, 'qs/edit.html', {'form': form})



@login_required
def edit_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    question = solution.question

    if request.method == "POST":
        form = SolutionForm(request.POST, instance=solution)
        if form.is_valid():
            solution = form.save(commit=False)
            # solution.author = request.user
            solution.save()
            return redirect('qs.views.detail', pk=question.pk)
    else:
        form = SolutionForm(instance=solution)
    return render(request, 'qs/node/edit_solution.html', {'question': question,  'form': form})

@login_required
def del_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    question = solution.question
    solution.delete()
    return redirect('qs.views.detail', pk=question.pk)



@login_required
def draft_list(request):
    # posts = Question.objects.filter(published_date__isnull=True)
    posts = Question.objects.filter(published_date__isnull=True).order_by('-created')
    return render(request, 'qs/draft_list.html', {'posts': posts})

@login_required
def draft_detail(request, pk):
    post = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = None
            if 'publish' in request.POST:
                post.publish()
                return redirect('qs.views.index')
            elif 'discard' in request.POST:
                post.delete()
            else:
                post.save()
            return redirect('qs.views.draft_list')
    else:
        form = QuestionForm(instance=post)
    return render(request, 'qs/node/draft_detail.html', {'form': form})

@login_required
def post_vote(request, pk):
    post = get_object_or_404(Question, pk=pk)
    post.count_vote += 1
    post.save()


    print(post.author)
    user = get_object_or_404(User, username=post.author)
    # user = get_object_or_404(User, username__contains=post.author)
    # user.voted += 5
    # user.save()
    print(dir(user))
    return redirect('qs.views.detail', pk=pk)




def full_search(request):
    """全局搜索"""
    keywords = request.GET['q']
    sform = SearchForm(request.GET)
    posts = sform.search()
    return render(request, 'qs/post_search_list.html',
                  {'posts': posts, 'list_header': '关键字 \'{}\' 搜索结果'.format(keywords)})