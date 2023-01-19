from datetime import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from django import forms

from ..core.helpers.form_helpers import set_field_properties
from ..core.mixins.form_mixin import FormMixin
from .models import Bike, BikeInfo, Component, ComponentStatistic


class ComponentForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)


class ComponentStatisticForm(forms.ModelForm):
    class Meta:
        model = ComponentStatistic
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        bike_slug = kwargs.pop('bike_slug')
        component_pk = kwargs.pop('component_pk')

        super().__init__(*args, **kwargs)

        self.fields['bike'].initial = Bike.objects.related().get(slug=bike_slug)
        self.fields['component'].initial = Component.objects.related().get(pk=component_pk)
        # self.fields['bike'].disabled = True
        # self.fields['bike'].widged = forms.HiddenInput()
        # self.fields['bike'].disabled = True
        # self.fields['bike'].widged = forms.HiddenInput()

        self.helper = FormHelper()
        set_field_properties(self, self.helper)



class BikeForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Bike
        fields = [
            'date',
            'full_name',
            'short_name',
            'main',
            'retired',
        ]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].initial = datetime.now()

        self.helper = FormHelper()
        set_field_properties(self, self.helper)

        self.helper.form_show_labels = True

        self.fields['date'].label = ''
        self.fields['full_name'].label = ''
        self.fields['short_name'].label = ''
        self.fields['main'].label = 'Pagrindinis'
        self.fields['retired'].label = 'Parduotas'

    def clean_main(self):
        _main = self.cleaned_data.get('main')

        qs = Bike.objects.items().filter(main=True)

        # exclude self if update
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if _main and qs.count() > 0:
            raise forms.ValidationError('Gali būti tik vienas pagrindinis dviratis!')

        return _main

    def clean_retired(self):
        _main = self.cleaned_data.get('main')
        _retired = self.cleaned_data.get('retired')

        if _main and _retired:
            raise forms.ValidationError('Pagrindio dviračio negalima žymėti kaip Parduotas!')

        return _retired


class BikeInfoForm(forms.ModelForm):
    class Meta:
        model = BikeInfo
        fields = '__all__'
        widgets = {
            'bike': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
