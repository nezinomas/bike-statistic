from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView

from . import forms, models


def test(request):
    return render(
        request,
        'reports/test.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


class ViewData(CreateView):
    model = models.Data
    form_class = forms.DataForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['formset'] = forms.DataFormset()
        context['helper'] = forms.DataFormSetHelper()

        return context

    def post(self, request, *args, **kwargs):
        formset = forms.DataFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset, **kwargs):
        formset.save()
        return super().form_valid(form=formset)

    def get_success_url(self):
        return reverse_lazy('reports:index')

