from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from .models import CustomUser


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already taken.')
                else:
                    form.save()

        context = {'form': form}
        return render(request, 'accounts/signin.html', context)
