from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView

from .forms import SignUpForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signup_done')
    template_name = 'accounts/signup.html'


class SignUpDoneView(TemplateView):
    template_name = 'accounts/signup_done.html'


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'country',
        'city',
    ]
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.slug})


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
