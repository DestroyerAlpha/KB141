from django.urls import path
from . import views

urlpatterns = [
    #website-home is set as login redirect in settings.py
    path('', views.home, name='website-home'),
    #path('ufilter/', views.UserFilterView.get_queryset, name='u_filter'),
    path('rsfilter/', views.rs_filter, name='rsfilter'),
]
