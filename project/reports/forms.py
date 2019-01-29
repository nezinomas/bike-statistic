from django import forms

from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput

from . import models
from ..core.helpers.form_helpers import set_field_properties


class DataForm(forms.ModelForm):
    class Meta:
        model = models.Data
        fields = '__all__'
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'checked': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
