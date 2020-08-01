from django.urls import path
from .views import (
    PostListView,
)
from . import views

urlpatterns = [
    path('', views.user_post, name="feed"),
]