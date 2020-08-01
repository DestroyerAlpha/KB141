from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    TextPostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostLikeView,
    CommentLikeView,
    add_comment_to_post,
    PostSaveView,
    UserPostSaveView,
    PaperPostCreateView,
)
from . import views

urlpatterns = [
    path('', views.user_post, name="feed"),
    path('create/', TextPostCreateView.as_view(), name='text-post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/like/<int:postid>/', PostLikeView, name='like'),
    path('post/like/comment/<int:commentid>/<int:postid>', CommentLikeView, name='comment-like'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('save/<int:postid>/<int:num>', views.PostSaveView, name='save'),
    path('bookmarks', UserPostSaveView.as_view(), name = "bookmark"),
    path('create/paper/<int:paperid>', PaperPostCreateView.as_view(), name='paper-post-create'),
]