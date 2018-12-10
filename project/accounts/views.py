from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # after user creation, automatically login
            # auth_login(request, user)
            return redirect('goals:home')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})
