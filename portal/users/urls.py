from django.urls import path
from . import views
from feed.views import UserPostView

urlpatterns = [
    path('', views.user_profile, name='user-profile'),
    path('student_detail/', views.student_detail, name='student_detail'),
    path('corporate_detail/', views.corporate_detail, name='corporate_detail'),
    path('student_register/', views.student_register, name='student_register'),
    path('corporate_register/', views.corporate_register, name='corporate_register'),
    path('profile/feed/<str:username>/', UserPostView.as_view(), name='user-feed')
]
