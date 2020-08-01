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


def user_post(request):
    users = User.objects.filter(username=request.user.username)
    try:
        profile = Profile_student.objects.get(user__in = users)
    except:
        profile = Profile_corporate.objects.get(user__in = users)
    users = profile.authors_followed.all()
    authors_followed_list_ids = [person.id for person in request.user.profile.authors_followed.all()]

    recommended_users = Profile_student.objects.filter(rating__gte=request.user.profile.rating-300).exclude(id__in=authors_followed_list_ids)
    context = {'user': request.user, 'posts': Post.objects.filter(author__in=users).order_by('-date_posted'), 'recommended_users': recommended_users}

    print(authors_followed_list_ids, '*'*10)
    return render(request, 'feed/feed.html', context)

