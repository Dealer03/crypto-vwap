from django.urls import path
<<<<<<< HEAD
from .views import upload_file
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
=======
from .views import parse_html_to_csv

urlpatterns = [
    path('parse/', parse_html_to_csv, name='parse_html_to_csv'),
>>>>>>> 9f6d1d93f71c8fffdbf19923c880713921b24c12
]
