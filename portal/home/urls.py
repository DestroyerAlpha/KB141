from django.urls import path
from . import views

urlpatterns = [
    #website-home is set as login redirect in settings.py
    path('', views.home, name='website-home'),
]
