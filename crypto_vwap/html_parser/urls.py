from django.urls import path
from .views import upload_file, download_csv_file, upload_csv_file
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('download/', download_csv_file, name='download_csv_file'),
    path('upload_csv/', upload_csv_file, name='upload_csv_file'),
]
