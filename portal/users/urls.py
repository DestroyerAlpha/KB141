from django.urls import path
from . import views
from feed.views import UserPostView

urlpatterns = [
    path('', views.user_profile, name='user-profile'),
]
