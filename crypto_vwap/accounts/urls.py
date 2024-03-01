from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('remove-duplicates/', views.remove_duplicate_transactions,
         name='remove_duplicates'),
    path('delete/', views.delete_all_transactions,
         name='delete_all_transactions'),
    path('reset_password/', views.CustomPasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_done/', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
