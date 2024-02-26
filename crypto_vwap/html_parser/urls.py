from django.urls import path
from .views import upload_files, download_csv_file, home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('download/', download_csv_file, name='download_csv_file'),
    path('upload_files/', upload_files, name='upload_files'),
]
