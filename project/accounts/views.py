from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm

from . import forms

def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            # after user creation, automatically login
            # auth_login(request, user)
            return redirect('goals:home')
    else:
        form = forms.SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})
