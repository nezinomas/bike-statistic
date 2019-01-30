from django import forms

from crispy_forms.helper import FormHelper

from .models import Goal
from ..core.helpers.form_helpers import set_field_properties


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
