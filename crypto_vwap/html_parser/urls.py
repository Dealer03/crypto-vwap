from django.urls import path
from .views import parse_html_to_csv

urlpatterns = [
    path('parse/', parse_html_to_csv, name='parse_html_to_csv'),
]
