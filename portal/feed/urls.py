from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    TextPostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostLikeView,
    add_comment_to_post,
    PaperPostCreateView,
)
from . import views

urlpatterns = [
    path('', views.user_post, name="feed"),
    path('create/', TextPostCreateView.as_view(), name='text-post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/like/<int:postid>/', PostLikeView, name='like'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('create/paper/<int:paperid>', PaperPostCreateView.as_view(), name='paper-post-create'),
]