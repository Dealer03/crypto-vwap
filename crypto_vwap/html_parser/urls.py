from django.urls import path
from .views import upload_file, home
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('', views.home, name='home'),
]
