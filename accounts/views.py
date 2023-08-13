from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signup_done')
    template_name = 'accounts/signup.html'


class SignUpDoneView(TemplateView):
    template_name = 'accounts/signup_done.html'


class CustomLoginView(views.LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'


class CustomPasswordChangeView(views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'


class CustomPasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class CustomPasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    html_email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'


class CustomPasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'


class CustomPasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'
