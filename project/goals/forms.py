from datetime import datetime

from bootstrap_datepicker_plus.widgets import YearPickerInput
from crispy_forms.helper import FormHelper
from django import forms

from ..core.helpers.form_helpers import set_field_properties
from ..core.mixins.form_mixin import FormMixin
from .models import Goal


class GoalForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['year', 'goal']
        widgets = {
            'year': YearPickerInput(
                options={
                    "format": "YYYY",
                    "locale": "lt",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = datetime.now()

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
