from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_request, name='home_request'),
    path('new_search', views.new_search, name='new_search'),


]