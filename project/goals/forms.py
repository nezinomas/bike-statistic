from datetime import datetime

from bootstrap_datepicker_plus.widgets import YearPickerInput
from crispy_forms.helper import FormHelper
from django import forms

from ..core.lib import utils
from ..core.mixins.form_mixin import FormMixin
from .models import Goal


class GoalForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['year', 'goal']
        widgets = {
            'year': YearPickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = datetime.now().year

        self.helper = FormHelper()

    def clean(self):
        cleaned_data = super().clean()
        utils.clean_year_picker_input("year", self.data, cleaned_data, self.errors)

        year = cleaned_data.get("year")

        # if update
        if self.instance.pk and 'year' not in self.changed_data:
            return cleaned_data

        # if new record
        qs = Goal.objects.related().filter(year=year)
        if qs.exists():
            self.add_error('year', f"{year} already has a goal.")

        return cleaned_data
