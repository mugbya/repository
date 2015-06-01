# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404 ,render,redirect
from django.views.generic import ListView, CreateView, FormView, TemplateView
from django.contrib.auth import authenticate, login
from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput
from django.utils.six import BytesIO


from .forms import QuestionForm, SolutionForm

from .models import *

class IndexView(TemplateView):
    template_name = 'qs/index.html'

    def get_context_data(self, **kwargs):
        question_list = Question.objects.all()
        return {
            'post_latest': question_list,
        }

# class DetailView(ListView):
#     model = Question
#     template_name = 'qs/node/detail.html'
#
#     def get_queryset(self):
#         all_replies = super(DetailView, self).get_queryset()
#         replies_belong_to_this_post = all_replies.filter(question=self.kwargs['pk']).order_by('pk')
#         return replies_belong_to_this_post
#
#     def get_context_data(self, **kwargs):
#         context = super(DetailView, self).get_context_data(**kwargs)
#         context['post'] = get_object_or_404(Question, pk=self.kwargs['pk'])
#         return context


class CreateView(CreateView):
    model = Question
    fields = ['title', ]
    template_name = 'qs/edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user if self.request.user.is_authenticated() else None
        form.instance.node = self.get_node()
        return super(CreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        return context

    def get_form_class(self):
        if self.request.user.is_superuser:
            self.fields = ['title',  ]
        elif self.request.user.is_authenticated():
            self.fields = ['title',  ]

        return super(CreateView, self).get_form_class()


def detail(request, pk):
    detail_qs = get_object_or_404(Question, pk=pk) #Question.objects.get(id = 4)
    solution = detail_qs.solution_set
    solution_list = solution.all()
    solution_count = solution.count()
    return render(request, 'qs/node/detail.html', {'detail_qs': detail_qs, 'solutions': solution_list, 'count': solution_count })

def new_qs(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('qs.views.detail', pk=post.pk)
    else:
        form = QuestionForm()
    return render(request, 'qs/edit.html', {'form': form})

def edit_qs(request, pk):
    post = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('qs.views.detail', pk=post.pk)
    else:
        form = QuestionForm(instance=post)
    return render(request, 'qs/edit.html', {'form': form})

# def save_solution(requset, pk):
#     question = get_object_or_404(Question, pk=pk)


def edit_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    question = solution.question

    if request.method == "POST":
        form = SolutionForm(request.POST, instance=solution)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.author = request.user
            solution.save()
            return redirect('qs.views.detail', pk=question.pk)
    else:
        form = SolutionForm(instance=solution)
    return render(request, 'qs/node/edit_solution.html', {'question': question,  'form': form})

def reply(request):
    pass

def draft(request):
    posts = Question.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})