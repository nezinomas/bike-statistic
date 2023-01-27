import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from vanilla import (CreateView, DeleteView, DetailView, ListView,
                     RedirectView, TemplateView, UpdateView)


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


# ---------------------------------------------------------------------------------------
#                                                                                  Mixins
# ---------------------------------------------------------------------------------------
class CreateUpdateMixin:
    hx_trigger_django = None
    detail_view = None

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form)

        if self.detail_view:
            rendered = render_to_string(
                self.detail_view.template_name, {'object': self.object}, self.request)
            return HttpResponse(rendered)

        if self.hx_trigger_django:
            response.status_code = 204
            trigger_client_event(response=response, name=self.hx_trigger_django, params={})
            return response

        return response


class DeleteMixin:
    hx_trigger_django = None
    hx_redirect = None

    def get_hx_trigger_django(self):
        return self.hx_trigger_django

    def get_hx_redirect(self):
        return self.hx_redirect

    def post(self, *args, **kwargs):
        if not self.get_object():
            return HttpResponse()

        super().post(*args, **kwargs)

        if hx_redirect := self.get_hx_redirect():
            return HttpResponseClientRedirect(hx_redirect)

        return httpHtmxResponse(self.get_hx_trigger_django())



# ---------------------------------------------------------------------------------------
#                                                                            Views Mixins
# ---------------------------------------------------------------------------------------
class CreateViewMixin(LoginRequiredMixin, CreateUpdateMixin, CreateView):
    pass


class UpdateViewMixin(LoginRequiredMixin, CreateUpdateMixin, UpdateView):
    pass


class DeleteViewMixin(LoginRequiredMixin, DeleteMixin, DeleteView):
    pass


class DetailViewMixin(LoginRequiredMixin, DetailView):
    pass


class ListViewMixin(LoginRequiredMixin, ListView):
    pass


class TemplateViewMixin(LoginRequiredMixin, TemplateView):
    pass


class RedirectViewMixin(LoginRequiredMixin, RedirectView):
    pass
