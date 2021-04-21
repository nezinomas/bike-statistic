from datetime import date

from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput
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


class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=MonthPickerInput().start_of('event days'),
    )
    end_date = forms.DateField(
        widget=MonthPickerInput().end_of('event days'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if not isinstance(start, date) or not isinstance(end, date):
            raise forms.ValidationError('Invalid start or end date.')

        if start > end:
            raise forms.ValidationError('End date is greater than start date.')
