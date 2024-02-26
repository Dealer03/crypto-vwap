from django.urls import path
from .views import upload_html_file, download_csv_file, upload_csv_file, home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('download/', download_csv_file, name='download_csv_file'),
    path('upload_csv/', upload_csv_file, name='upload_csv_file'),
    path('upload_html/', upload_html_file, name='upload_html_file')
]
