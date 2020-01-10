from datetime import datetime

from bootstrap_datepicker_plus import DatePickerInput
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
        widgets = {
            'bike': forms.HiddenInput(),
            'component': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)


class BikeForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['date', 'full_name', 'short_name']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].initial = datetime.now()

        self.helper = FormHelper()
        set_field_properties(self, self.helper)


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
