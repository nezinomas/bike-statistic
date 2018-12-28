from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Component, ComponentStatistic
from .forms import ComponentForm


def index(request):
    return render(
        request,
        'bikes/index.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


def component_list(request):
    components = Component.objects.all()
    return render(request, 'bikes/component_list.html', {'components': components})

def component_create(request):
    data = {}

    if request.method == 'POST':
        form = ComponentForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = ComponentForm()


    context = {'form': form}
    html_form = render_to_string(
        template_name='bikes/includes/partial_component_create.html',
        context=context,
        request=request
    )

    return JsonResponse({'html_form': html_form})
