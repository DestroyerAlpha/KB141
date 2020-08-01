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


class PostDetailView(DetailView):
    model = Post


class TextPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    def form_valid(self, form):
        try:
            profile = Profile_student.objects.get(user = self.request.user)
        except:
            profile = Profile_corporate.objects.get(user = self.request.user)
        form.instance.author = profile
        form.instance.paper = None
        return super().form_valid(form)

class CustomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Abstract"
    class Meta:
        model = Post
        fields = ['content']

class PaperPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomForm

    def form_valid(self, form, *args, **kwargs):
        paperid = self.kwargs['paperid']
        papers = research_paper.objects.get(id = paperid)
        form.instance.author = self.request.user.profile
        form.instance.paper = papers
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        elif self.request.user.corporate_profile == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/feed/'

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        elif self.request.user.corporate_profile == post.author:
            return True
        return False


