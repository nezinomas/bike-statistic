from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView

# from bootstrap_datepicker_plus import DateTimePickerInput
from django.db import transaction

from . import forms, models


# class DataView(ListView):
#     model = models.Data
#     form_class = forms.DataFormset
#     template_name = 'reports/data_form.html'

#     # def get_object(self):
#     #     return get_object_or_404(models.Data, pk=1)

def test(request):
    return render(
        request,
        'reports/test.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )

def index(request):
    # return render(
    #     request,
    #     'bikes/index.html',
    #     context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    # )
    formset = modelformset_factory(models.Data, exclude=(), extra=1, form=forms.DataForm)

    if request.method == 'POST':
        f = formset(request.POST)
        if f.is_valid():
            f.save()
            # do something
            return redirect('reports:index')
    else:
        f = formset()

    helper = forms.DataFormSetHelper()

    return render(
        request,
        "reports/data_form.html",
        {"formset": f, 'helper': helper },
        # {"forms": f, },
    )


class ViewData(CreateView):
    model = models.Data
    form_class = forms.DataForm
    success_url = reverse_lazy('reports:index1')
    # success_url = 'index1'

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

    # def get_success_url(self):
    #     return reverse_lazy('reports:index1')

