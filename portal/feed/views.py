from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from .forms import CommentForm
from users.models import Profile_student, Profile_corporate
from ResearchPaper.models import research_paper

# Create your views here.

class PostListView(ListView):
    model = Post
    # template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']



class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed/feed.html'
    context_object_name = 'posts'
    poster = Post
    def get_queryset(self):
        users = User.objects.filter(username=self.request.user.username)
        try:
            profile = Profile_student.objects.get(user__in = users)
        except:
            profile = Profile_corporate.objects.get(user__in = users)
        users = profile.authors_followed.all()
        poster = Post.objects.filter(author__in = users).order_by('-date_posted')
        return poster


