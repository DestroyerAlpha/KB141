from django.urls import path
from . import views

urlpatterns = [
    path('add_paper/', views.research_paper, name='research_paper'),
]
