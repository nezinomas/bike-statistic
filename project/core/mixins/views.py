import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from vanilla import CreateView, DetailView, ListView, TemplateView, UpdateView


def rendered_content(request, view_class, **kwargs):
    # update request kwargs
    request.resolver_match.kwargs.update({**kwargs})

    return (
        view_class
        .as_view()(request, **kwargs)
        .rendered_content
    )


def httpHtmxResponse(hx_trigger_name=None, status_code=204):
    headers = {}
    if hx_trigger_name:
        headers = {
            'HX-Trigger': json.dumps({hx_trigger_name: None}),
        }

    return HttpResponse(
        status=status_code,
        headers=headers,
    )


class CreateUpdateMixin():
    hx_trigger_django = None
    hx_trigger_form = None
    hx_redirect = None

    def get_hx_trigger_django(self):
        # triggers Htmx to reload container on Submit button click
        # triggering happens many times
        return self.hx_trigger_django or None

    def get_hx_trigger_form(self):
        # triggers Htmx to reload container on Close button click
        # triggering happens once
        return self.hx_trigger_form or None

    def get_hx_redirect(self):
        return self.hx_redirect

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form)

        if not self.request.htmx:
            return response

        self.hx_redirect = self.get_hx_redirect()

        if self.hx_redirect:
            # close form and redirect to url with hx_trigger_django
            return HttpResponseClientRedirect(self.hx_redirect)

        # close form and reload container
        response.status_code = 204
        if trigger := self.get_hx_trigger_django():
            trigger_client_event(response=response, name=trigger, params={})
        return response


class CreateViewMixin(LoginRequiredMixin, CreateUpdateMixin, CreateView):
    pass


class UpdateViewMixin(LoginRequiredMixin, CreateUpdateMixin, UpdateView):
    pass


class DetailViewMixin(LoginRequiredMixin, DetailView):
    pass


class ListViewMixin(LoginRequiredMixin, ListView):
    pass


class TemplateViewMixin(LoginRequiredMixin, TemplateView):
    pass
