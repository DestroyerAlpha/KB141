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

class UserPostSaveView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed/bookmarks.html'
    context_object_name = 'posts'

class UserPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/user_feed.html'
    context_object_name = 'posts'
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        try:
            profile = Profile_student.objects.get(user = user)
        except:
            profile = Profile_corporate.objects.get(user = user)
        return Post.objects.filter(author=profile).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super(UserPostView, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        try:
            profile = Profile_student.objects.get(user = user)
        except:
            profile = Profile_corporate.objects.get(user = user)
        context['user_profile'] = profile
        return context

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

def PostLikeView(request, postid):
    post = Post.objects.get(id=postid)
    if request.user in post.post_like.all():
        post.post_like.remove(request.user)
        
        # update rating of author
        if post.paper != None:
            try:
                profile = Profile_student.objects.get(user = request.user)
            except:
                profile = Profile_corporate.objects.get(user = request.user)
            post.paper.liked_by.remove(profile)
            for author in post.paper.authors.all():
                author.rating -= 100
            author.save()
    else:
        post.post_like.add(request.user)

        # update rating of author
        
        if post.paper != None:
            try:
                profile = Profile_student.objects.get(user = request.user)
            except:
                profile = Profile_corporate.objects.get(user = request.user)
            post.paper.liked_by.add(profile)
            for author in post.paper.authors.all():
                author.rating += 100
            author.save()
    return redirect('post-detail', post.id)

def CommentLikeView(request, commentid, postid):
    comment = Comment.objects.get(id=commentid)
    if request.user in comment.comment_like.all():
        comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)
    return redirect('post-detail', postid)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_post = post
            comment.comment_author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'feed/add_comment_to_post.html', {'form': form})

def PostSaveView(request, postid, num):
    post = Post.objects.get(id=postid)
    if request.user in post.post_save.all():
        post.post_save.remove(request.user)
    else:
        post.post_save.add(request.user)
    if num == 1:
        return redirect('feed')
    elif num == 2:
        return redirect('bookmark')
    else:
        user = User.objects.get(id=num)
        return redirect('user-feed', user.username)
