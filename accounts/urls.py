from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.urls import path

from .views import CustomLoginView, CustomLogoutView, DashboardView, SignInView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
