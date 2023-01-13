from datetime import date

from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from django import forms

from ..bikes.models import Bike
from ..core.helpers.form_helpers import set_field_properties
from ..core.mixins.form_mixin import FormMixin
from . import models
from .helpers import view_data_helper as helper


class DataForm(FormMixin, forms.ModelForm):
    class Meta:
        model = models.Data
        fields = [
            'bike',
            'date',
            'distance',
            'time',
            'temperature',
            'ascent',
            'descent',
            'max_speed',
            'cadence',
            'heart_rate',
            'checked',
        ]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'checked': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bike'].queryset = Bike.objects.items().filter(retired=False)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)

    def save(self, commit=True):
        self.instance.checked = 'y'
        return super().save(commit)

class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(),
    )
    end_date = forms.DateField(
        widget=DatePickerInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].initial = helper.format_date(day=1)
        self.fields['end_date'].initial = helper.format_date()

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
