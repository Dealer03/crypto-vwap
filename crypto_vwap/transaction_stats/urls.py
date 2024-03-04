from django.urls import path
from . import views

urlpatterns = [
    path('holdings/', views.holdings, name='holdings'),
]
