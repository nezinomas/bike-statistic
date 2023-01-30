from datetime import date, timedelta

from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from django import forms

from ..bikes.models import Bike
from ..core.helpers.form_helpers import set_field_properties
from ..core.mixins.form_mixin import FormMixin
from . import models


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
        ]
        widgets = {
            'date': DatePickerInput(),
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

        self.fields['start_date'].initial = date.today() - timedelta(20)
        self.fields['end_date'].initial = date.today()

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
