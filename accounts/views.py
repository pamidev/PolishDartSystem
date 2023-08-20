from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
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
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = [
        'email',
        'first_name',
        'last_name',
        'country',
        'city',
        'phone',
    ]
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile_edit'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


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
