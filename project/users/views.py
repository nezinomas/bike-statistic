from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse

from .forms import ExternalUserForm


class CustomLogin(auth_views.LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class Logout(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse("users:login"))

        return response


@login_required
def sync_update(request):
    form = ExternalUserForm(request.POST or None, instance=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()

    template = 'users/sync.html'
    context = {
        'form': form,
        'password': request.user.garmin_password[:50],
    }
    return render(request, template, context)
