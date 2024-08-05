from datetime import datetime, timedelta

from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from crispy_forms.helper import FormHelper
from django import forms
from django.utils.timezone import make_aware

from ..bikes.models import Bike
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
            'date': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bike'].queryset = Bike.objects.items().filter(retired=False)

        self.helper = FormHelper()

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

        now = make_aware(datetime.now())
        self.fields['start_date'].initial = now - timedelta(20)
        self.fields['end_date'].initial = now

        self.helper = FormHelper()
        self.helper.form_show_labels = False