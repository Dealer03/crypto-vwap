from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_options, name='upload_options'),
    path('upload/html/', views.upload_html_file, name='html_upload'),
    path('upload/csv/', views.upload_csv_file, name='csv_upload'),
]
