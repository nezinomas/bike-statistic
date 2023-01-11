import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from vanilla import ListView, TemplateView


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


class DetailViewMixin(LoginRequiredMixin, DetailView):
    pass


class ListViewMixin(LoginRequiredMixin, ListView):
    pass


class TemplateViewMixin(LoginRequiredMixin, TemplateView):
    pass
