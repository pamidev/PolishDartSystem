from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'


@method_decorator(login_required, name='dispatch')
class LogOutView(TemplateView):
    template_name = 'accounts/logout.html'
