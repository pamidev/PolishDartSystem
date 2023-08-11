from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class SignInView(TemplateView):
    template_name = 'accounts/register.html'


class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'
