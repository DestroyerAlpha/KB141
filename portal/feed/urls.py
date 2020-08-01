from django.urls import path
from .views import (
    UserPostListView,
)
from . import views

urlpatterns = [
    path('', UserPostListView.as_view(), name="feed"),
]